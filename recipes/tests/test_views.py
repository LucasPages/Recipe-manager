from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.core.files.images import ImageFile
from recipes.models import Recipe, Tag, Ingredient
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
        recipe_pasta.picture = ImageFile(open('media/photo_recipes/eggplant_sm.jpg', 'rb'), 
                                         name="eggplant_sm.jpg")
        recipe_pasta.save()

        response = TestListViewData.client.get(reverse('recipes:list'))
        self.assertContains(response, text='<span class="italic">No picture</span>', count=1)

        os.remove(recipe_pasta.picture.path)


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
    pass


class TestUpdateRecipe(TestCase):
    pass