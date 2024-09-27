from django.urls import path
from recipes import views

app_name = "recipes"
urlpatterns = [
    path('', views.ListRecipes.as_view(), name="list"),
    path('create/', views.CreateRecipe.as_view(), name='create'),
    path('update/<int:pk>', views.UpdateRecipe.as_view(), name='update'),
    path('delete/<int:pk>', views.DeleteRecipe.as_view(), name='delete'),
    path('<int:pk>/', views.RecipeDetail.as_view(), name="detail"),
    path('tag/<slug:tag>', views.TagDetail.as_view(), name='tag'),
    path(
        'ingredient-autocomplete', 
         views.IngredientAutocomplete.as_view(create_field='name', validate_create=True), name='ingredient-autocomplete'
         ),
    path(
        'tag-autocomplete', 
         views.TagAutocomplete.as_view(create_field='tag', validate_create=True), 
         name='tag-autocomplete'
         ),
]
