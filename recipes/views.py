from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.db.models import Q
from recipes import models
from recipes import forms
from dal import autocomplete

# Create your views here.

class IngredientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return models.Ingredient.objects.all()


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return models.Tag.objects.all()


class CreateRecipe(CreateView):
    model = models.Recipe
    form_class = forms.CreateRecipe

    def post(self, request, *args, **kwargs):
        form = forms.CreateRecipe(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            try:
                recipe.picture = form.files['Data']
            except:
                pass
            recipe.save()

            return redirect(recipe)
        else:
            self.form_invalid(form)


class UpdateRecipe(UpdateView):
    model = models.Recipe
    form_class = forms.CreateRecipe

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        form = forms.CreateRecipe(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            try:
                recipe.picture = form.files['Data']
            except:
                pass
            recipe.save()
            return redirect(recipe)
        else:
            return self.form_invalid()


class DeleteRecipe(DeleteView):
    model = models.Recipe

    def get_success_url(self):
        return reverse('recipes:list')

class ListRecipes(ListView):
    model = models.Recipe
    ordering = ["name"]

    def get_queryset(self) -> QuerySet[models.Recipe]:
        result = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            result = models.Recipe.objects.filter(Q(name__iexact=query) | Q(name__istartswith=query) | Q(tags__tag__iexact=query)).distinct()
        return result


class RecipeDetail(DetailView):
    model = models.Recipe


class TagDetail(DetailView):
    model = models.Tag
    slug_field = 'tag'
    slug_url_kwarg = 'tag'
    
    def get_slug_field(self):
        return 'tag'

