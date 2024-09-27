from django_webtest import WebTest
from django.urls import reverse
from django.test import Client

from recipes.forms import CreateRecipe
from recipes.models import Recipe, Ingredient, Tag

import re, os


class TestCreateForm(WebTest):
    def setUp(self):
        Ingredient.objects.create(name="Pasta")
        Ingredient.objects.create(name="Pesto")

        Tag.objects.create(tag="pasta")
        Tag.objects.create(tag="saucy")


    def test_form_valid_data(self):
        form = CreateRecipe(
            data={
            'name': 'Pesto pasta',
            'ingredients': [Ingredient.objects.get(name="Pasta"), Ingredient.objects.get(name="Pesto")],
            'tags': [Tag.objects.get(tag="pasta")],
            'instructions': 'Cook the pasta.\nMix in the pesto.',
            'notes': 'Add parmesan for extra flavour',
            }
        )
        
        self.assertTrue(form.is_valid())
        
        recipe = form.save(commit=False)
        recipe.picture = 'photo_recipes/eggplant_sm.jpg'
        recipe.save()

        recipe.ingredients.set([Ingredient.objects.get(name="Pasta"), Ingredient.objects.get(name="Pesto")])
        recipe.tags.set([Tag.objects.get(tag="pasta")])

        self.assertEqual(recipe.name, 'Pesto pasta')
        self.assertEqual(recipe.instructions, 'Cook the pasta.\nMix in the pesto.')
        self.assertEqual(recipe.notes, 'Add parmesan for extra flavour')
        self.assertEqual(list(recipe.ingredients.all()), [Ingredient.objects.get(name="Pasta"), Ingredient.objects.get(name="Pesto")])
        self.assertEqual(list(recipe.tags.all()), [Tag.objects.get_or_create(tag="pasta")[0]])
        self.assertEqual(recipe.picture, 'photo_recipes/eggplant_sm.jpg')

    def test_blank_data(self):
        form = CreateRecipe({})

        self.assertFalse(form.is_valid())

        self.assertEqual(list(form.errors.keys()), ['name', 'ingredients', 'instructions'])
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['instructions'], ['This field is required.'])
        self.assertEqual(form.errors['ingredients'], ['This field is required.'])

    def test_form_success(self):
        page = self.app.get(reverse('recipes:create'))

        page.forms[1]['name'] = 'Pesto pasta'
        page.forms[1]['instructions'] = 'Cook pasta\nAdd pesto'
        page.forms[1]['ingredients'].force_value([Ingredient.objects.get(name="Pesto").pk])

        response = page.forms[1].submit()
        self.assertEqual(response.status_code, 302)
    
    def test_create_recipe_with_all_fields(self):
        client = Client()

        fields = {
            'name': 'Pesto pasta reborn',
            'instructions': "This how you do iiiit",
            'notes': "Add parmigianooooooo",
            'ingredients': [Ingredient.objects.get(name="Pasta").pk, Ingredient.objects.get(name="Pesto").pk],
            'tags': [Tag.objects.get(tag="pasta").pk, Tag.objects.get(tag="saucy").pk],
            'picture': open('/home/lucas/web/django_projects/recipe_manager/media/photo_recipes/hummus_sm.jpg', 'rb'),
        }

        response = client.post(
            reverse('recipes:create'),
            data=fields
        )
        recipe = Recipe.objects.last()

        self.assertRedirects(response, reverse('recipes:detail', kwargs={'pk': recipe.pk}))

        self.assertEqual(recipe.name, 'Pesto pasta reborn')
        self.assertEqual(recipe.instructions, 'This how you do iiiit')
        self.assertEqual(list(recipe.ingredients.all()), [Ingredient.objects.get(name="Pasta"), Ingredient.objects.get(name="Pesto")])
        self.assertEqual(list(recipe.tags.all()), [Tag.objects.get(tag="pasta"), Tag.objects.get(tag="saucy")])
        self.assertEqual(recipe.notes, "Add parmigianooooooo")

        pattern = r'([a-z]+)_[^_]+(.jpg)$'
        basename_file = re.sub(string=os.path.basename(recipe.picture.path), pattern=pattern, repl=r'\1\2')

        self.assertEqual(basename_file, 'hummus_sm.jpg')

        os.remove(recipe.picture.path)


class TestUpdateForm(WebTest):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        Ingredient.objects.create(name="Pesto")
        Ingredient.objects.create(name="Pasta")

        Tag.objects.create(tag="pasta")
        Tag.objects.create(tag="saucy")
        
    
    def setUp(self):
        recipe_pasta = Recipe.objects.create(
            name = "Pesto pasta",
            picture = None,
            instructions = "Cook the pasta.\nMix in the pesto.",
            notes = "Add parmesan for extra flavour"
        )

        recipe_pasta.ingredients.set([Ingredient.objects.get(name="Pasta"), Ingredient.objects.get(name="Pesto")])
        recipe_pasta.tags.set([Tag.objects.get(tag="pasta"), Tag.objects.get(tag="saucy")])
        recipe_pasta.save()

        self.data = {
            'name': 'Pesto pasta',
            'instructions': "Cook the pasta.\nMix in the pesto.",
            'notes': "Add parmesan for extra flavour",
            'ingredients': [Ingredient.objects.get(name="Pasta").pk, Ingredient.objects.get(name="Pesto").pk],
            'tags': [Tag.objects.get(tag="pasta").pk, Tag.objects.get(tag="saucy").pk],
            'picture': 'photo_recipes/eggplant_sm.jpg',
        }

    def test_update_name(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        self.data['name'] = 'la pastaaa'
        response = self.client.post(
            reverse('recipes:update', kwargs={'pk': recipe.pk}),
            data=self.data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:detail', kwargs={'pk': recipe.pk}))

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, 'La pastaaa')
        

    def test_update_ingredients(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        self.data['ingredients'] = [Ingredient.objects.get(name="Pasta").pk]
        response = self.client.post(
            reverse('recipes:update', kwargs={'pk': recipe.pk}),
            data=self.data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:detail', kwargs={'pk': recipe.pk}))

        recipe.refresh_from_db()
        self.assertEqual(list(recipe.ingredients.all()), [Ingredient.objects.get(name="Pasta")])

    def test_update_instructions(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        self.data['instructions'] = 'Cook pasta\nAdd pesto.'
        response = self.client.post(
            reverse('recipes:update', kwargs={'pk': recipe.pk}),
            data=self.data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:detail', kwargs={'pk': recipe.pk}))

        recipe.refresh_from_db()
        self.assertEqual(recipe.instructions, 'Cook pasta\nAdd pesto.')

    def test_update_notes(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        self.data['notes'] = 'Remove the pesto and eat raw'
        response = self.client.post(
            reverse('recipes:update', kwargs={'pk': recipe.pk}),
            data=self.data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:detail', kwargs={'pk': recipe.pk}))

        recipe.refresh_from_db()
        self.assertEqual(recipe.notes, 'Remove the pesto and eat raw')

    def test_update_tags(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        self.data['tags'] = [Tag.objects.get(tag="saucy").pk]
        response = self.client.post(
            reverse('recipes:update', kwargs={'pk': recipe.pk}),
            data=self.data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:detail', kwargs={'pk': recipe.pk}))

        recipe.refresh_from_db()
        self.assertEqual(list(recipe.tags.all()), [Tag.objects.get(tag="saucy")])
    
    def test_update_picture(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        with open('/home/lucas/web/django_projects/recipe_manager/media/photo_recipes/hummus_sm.jpg', 'rb') as image:
            self.data['picture'] = image
            response = self.client.post(
                reverse('recipes:update', kwargs={'pk': recipe.pk}),
                data=self.data,
                
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('recipes:detail', kwargs={'pk': recipe.pk}))

            pattern = r'([a-z]+)_[^_]+(.jpg)$'
            recipe.refresh_from_db()
            basename_file = re.sub(string=os.path.basename(recipe.picture.path), pattern=pattern, repl=r'\1\2')

            self.assertEqual(basename_file, 'hummus_sm.jpg')
            os.remove(recipe.picture.path)
