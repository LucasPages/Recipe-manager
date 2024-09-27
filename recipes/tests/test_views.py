from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.core.files.images import ImageFile
from recipes.models import Recipe, Tag, Ingredient
from recipes.forms import CreateRecipe
import os


class TestAbout(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('about')

    def test_about_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_manager/index.html')


class TestListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('home')

    def test_view_gets_both_names(self):
        # Both 'recipe:list' and 'home' use the ListView
        view_home = resolve('/')[0].__module__
        view_recipes = resolve('/recipes/')[0].__module__

        self.assertEqual(view_home, view_recipes)

    def test_listview_GET(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')


class TestListViewData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def setUp(self):
        recipe_pasta = Recipe.objects.create(
            name = "pesto pasta",
            picture = None,
            instructions = "Cook the pasta.\nMix in the pesto.",
            notes = "Add parmesan for extra flavour"
        )
        recipe_pasta.ingredients.set([Ingredient.objects.get_or_create(name="Pasta")[0], Ingredient.objects.get_or_create(name="Pesto")[0]])
        recipe_pasta.tags.set([Tag.objects.get_or_create(tag="pasta")[0]])

        recipe_salad = Recipe.objects.create(
            name = "chickpea salad",
            picture = None,
            instructions = "Mix all ingredients\nAdd lemon juice and olive oil dressing\nSalt and pepper to taste",
            notes = "Add croutons for crunch"
        )
        recipe_salad.ingredients.set([Ingredient.objects.get_or_create(name="tomato")[0], Ingredient.objects.get_or_create(name="cucumber")[0], Ingredient.objects.get_or_create(name="chickpea")[0], Ingredient.objects.get_or_create(name="")[0]])
        recipe_salad.tags.set([Tag.objects.get_or_create(tag="salad")[0], Tag.objects.get_or_create(tag="easy")[0]])

    def test_contains_two_recipes(self):
        count_data = Recipe.objects.filter().count()
        self.assertEqual(count_data, 2)

        response = TestListViewData.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['recipe_list'].count(), 2)

    def test_search_by_tag_function(self):
        count_data = Recipe.objects.filter().count()
        self.assertEqual(count_data, 2)

        response_search = TestListViewData.client.get(reverse('recipes:list'), {'search': 'easy'})
        self.assertEqual(response_search.status_code, 200)
        self.assertEqual(response_search.context['recipe_list'].count(), 1)

        response_search = TestListViewData.client.get(reverse('recipes:list'), {'search': 'Easy'})
        self.assertEqual(response_search.status_code, 200)
        self.assertEqual(response_search.context['recipe_list'].count(), 1)
    
    def test_search_by_name_function(self):
        count_data = Recipe.objects.filter().count()
        self.assertEqual(count_data, 2)

        response_search = TestListViewData.client.get(reverse('recipes:list'), {'search': 'pesto'})
        self.assertEqual(response_search.status_code, 200)
        self.assertEqual(response_search.context['recipe_list'].count(), 1)

        response_search = TestListViewData.client.get(reverse('recipes:list'), {'search': 'Pesto'})
        self.assertEqual(response_search.status_code, 200)
        self.assertEqual(response_search.context['recipe_list'].count(), 1)

    def test_no_image_correct(self):
        response = TestListViewData.client.get(reverse('recipes:list'))

        self.assertContains(response, text='<span class="italic">No picture</span>', count=2)

    def test_image_correct(self):
        recipe_pasta = Recipe.objects.get(name='Pesto pasta')
        recipe_pasta.picture = 'photo_recipes/eggplant_sm.jpg'
        recipe_pasta.save()

        response = TestListViewData.client.get(reverse('recipes:list'))
        self.assertContains(response, text='<span class="italic">No picture</span>', count=1)


class TestDetailViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
    
    def setUp(self):
        recipe_pasta = Recipe.objects.create(
            name = "pesto pasta",
            picture = None,
            instructions = "Cook the pasta.\nMix in the pesto.",
            notes = "Add parmesan for extra flavour"
        )
        recipe_pasta.ingredients.set([Ingredient.objects.get_or_create(name="Pasta")[0], Ingredient.objects.get_or_create(name="Pesto")[0]])
        recipe_pasta.tags.set([Tag.objects.get_or_create(tag="pasta")[0]])
    
    def test_detail_recipe_accessible(self):
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': Recipe.objects.get(name="Pesto pasta").pk}))
        self.assertEqual(response.status_code, 200)

    def test_detail_recipe_correct_template(self):
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': Recipe.objects.get(name="Pesto pasta").pk}))
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_detail_tag_accessible(self):
        response = self.client.get(reverse('recipes:tag', kwargs={'tag': Tag.objects.get(tag="pasta").tag}))
        self.assertEqual(response.status_code, 200)

    def test_detail_tag_correct_template(self):
        response = self.client.get(reverse('recipes:tag', kwargs={'tag': Tag.objects.get(tag="pasta").tag}))
        self.assertTemplateUsed(response, 'recipes/tag_detail.html')


class TestDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
    
    def setUp(self):
        recipe_pasta = Recipe.objects.create(
            name = "pesto pasta",
            picture = None,
            instructions = "Cook the pasta.\nMix in the pesto.",
            notes = "Add parmesan for extra flavour"
        )
        recipe_pasta.ingredients.set([Ingredient.objects.get_or_create(name="Pasta")[0], Ingredient.objects.get_or_create(name="Pesto")[0]])
        recipe_pasta.tags.set([Tag.objects.get_or_create(tag="pasta")[0]])

    def test_recipe_deleted(self):
        count_data = Recipe.objects.filter().count()
        self.assertEqual(count_data, 1)

        self.client.post(reverse('recipes:delete', kwargs={'pk': Recipe.objects.get(name="Pesto pasta").pk}))
        count_data = Recipe.objects.filter().count()
        self.assertEqual(count_data, 0)

    def test_success_url(self):
        response = self.client.post(reverse('recipes:delete', kwargs={'pk': Recipe.objects.get(name="Pesto pasta").pk}))
        self.assertRedirects(response, reverse('recipes:list'))

    
class TestCreateRecipe(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
    
    def test_create_page_accessible(self):
        response = self.client.get(reverse('recipes:create'))
        self.assertEqual(response.status_code, 200)
        
    def test_create_page_uses_correct_template(self):
        response = self.client.get(reverse('recipes:create'))
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')


class TestUpdateRecipe(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
    
    def setUp(self):
        recipe_pasta = Recipe.objects.create(
            name = "Pesto pasta",
            picture = None,
            instructions = "Cook the pasta.\nMix in the pesto.",
            notes = "Add parmesan for extra flavour"
        )
        recipe_pasta.ingredients.set([Ingredient.objects.get_or_create(name="Pasta")[0], Ingredient.objects.get_or_create(name="Pesto")[0]])
        recipe_pasta.tags.set([Tag.objects.get_or_create(tag="pasta")[0]])
    
    def test_update_page_accessible(self):
        recipe = Recipe.objects.get(name='Pesto pasta')
        response = self.client.get(reverse('recipes:update', kwargs={'pk': recipe.pk}))

        self.assertEqual(response.status_code, 200)
    
    def test_update_page_uses_correct_template(self):
        recipe = Recipe.objects.get(name='Pesto pasta')
        response = self.client.get(reverse('recipes:update', kwargs={'pk': recipe.pk}))

        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
    
    def test_data_filled(self):
        recipe_pasta = Recipe.objects.get(name='Pesto pasta')
        recipe_pasta.picture = 'photo_recipes/eggplant_sm.jpg'
        recipe_pasta.save()

        response = self.client.get(reverse('recipes:update', kwargs={'pk': recipe_pasta.pk}))
        
        self.assertEqual(response.context['form'].initial['name'], 'Pesto pasta')
        self.assertEqual(response.context['form'].initial['instructions'], 'Cook the pasta.\nMix in the pesto.')
        self.assertEqual(response.context['form'].initial['notes'], 'Add parmesan for extra flavour')
        self.assertEqual(response.context['form'].initial['tags'], [Tag.objects.get_or_create(tag="pasta")[0]])
        self.assertEqual(response.context['form'].initial['picture'], recipe_pasta.picture)
        self.assertEqual(response.context['form'].initial['ingredients'], [Ingredient.objects.get_or_create(name="Pasta")[0], Ingredient.objects.get_or_create(name="Pesto")[0]])
