from django import forms
import django
from recipes import models
from dal import autocomplete


class CreateRecipe(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = '__all__'
        widgets = {
            'ingredients' : autocomplete.ModelSelect2Multiple(url='recipes:ingredient-autocomplete'),
            'tags' : autocomplete.ModelSelect2Multiple(url='recipes:tag-autocomplete', attrs={'placeholder': 'Select tags for this recipe'}),
            'name': forms.TextInput(attrs={'placeholder': 'Recipe name', 'autocomplete': 'off'}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Write each instruction on a new line', 'autocomplete': 'off'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Personal notes, if relevant', 'autocomplete': 'off'})
        }
