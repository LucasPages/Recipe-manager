from django.test import TestCase
from recipes.models import Ingredient, Tag, Recipe


class IngredientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Ingredient.objects.create(name="oignon")
    
    def test_name_is_capitalized(self):
        query_result = Ingredient.objects.filter(name__iexact='oignon').values_list('name', flat=True)
        self.assertQuerySetEqual(query_result, ['Oignon'])
    
    def test_label_correct(self):
        oignon = Ingredient.objects.get(name="Oignon")
        name_field_label = oignon._meta.get_field('name').verbose_name
        self.assertEqual(name_field_label, 'name')


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(tag='Easy')
    
    def test_lowercase_name(self):
        query_result = Tag.objects.filter(tag__exact='easy').values_list('tag', flat=True)
        self.assertQuerySetEqual(query_result, ['easy'])
    
    def test_label_correct(self):
        easy = Tag.objects.get(tag="easy")
        tag_field_label = easy._meta.get_field('tag').verbose_name
        self.assertEqual(tag_field_label, 'tag')


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Ingredient.objects.create(name="Pasta")
        Ingredient.objects.create(name="Pesto")
        Tag.objects.create(tag="pasta")

    def setUp(self):
        recipe = Recipe.objects.create(
            name = "pesto pasta",
            picture = None,
            instructions = "Cook the pasta.\nMix in the pesto.",
            notes = "Add parmesan for extra flavour"
        )
        recipe.ingredients.set([Ingredient.objects.get(name="Pasta"), Ingredient.objects.get(name="Pesto")])
        recipe.tags.set([Tag.objects.get(tag="pasta")])
    
    def test_name_recipe(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        self.assertEqual(str(recipe), recipe.name)
    
    def test_name_is_capitalized(self):
        recipe = Recipe.objects.filter(name__iexact="pesto pasta").first()
        self.assertEqual(recipe.name, "Pesto pasta")
    
    def test_absolute_url_is_correct(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        self.assertEqual(recipe.get_absolute_url(), f"/recipes/{recipe.pk}/")

    ##### TEST LABELS

    def test_label_name_correct(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        name_field_label = recipe._meta.get_field("name").verbose_name
        self.assertEqual(name_field_label, 'name')

    def test_label_picture_correct(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        picture_field_label = recipe._meta.get_field("picture").verbose_name
        self.assertEqual(picture_field_label, 'picture')

    def test_label_instructions_correct(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        instructions_field_label = recipe._meta.get_field("instructions").verbose_name
        self.assertEqual(instructions_field_label, 'instructions')

    def test_label_ingredients_correct(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        ingredients_field_label = recipe._meta.get_field("ingredients").verbose_name
        self.assertEqual(ingredients_field_label, 'ingredients')

    def test_label_tags_correct(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        tags_field_label = recipe._meta.get_field("tags").verbose_name
        self.assertEqual(tags_field_label, 'tags')

    def test_label_notes_correct(self):
        recipe = Recipe.objects.get(name="Pesto pasta")
        notes_field_label = recipe._meta.get_field("notes").verbose_name
        self.assertEqual(notes_field_label, 'notes')
    
        