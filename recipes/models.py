from datetime import datetime
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.conf import settings
import os

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


class Tag(models.Model):
    tag = models.CharField(max_length=20)
    class Meta:
        ordering = ["tag"]

    def save(self, *args, **kwargs):
        self.tag = self.tag.lower()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.tag

class Recipe(models.Model):
    name = models.CharField(max_length=256)
    picture = models.ImageField(blank=True, upload_to='photo_recipes/')
    ingredients = models.ManyToManyField(Ingredient, related_name='recipe')
    instructions = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag, related_name='recipe')
    notes = models.TextField(blank=True)

    ordering = ["name"]

    def __str__(self):
        return self.name
    
    def clean(self) -> None:
        print(self)
        file = self.cleaned_data['file']
        print(file)
        if os.path.exists(file):
            print(f"{file} already exists")
            raise ValidationError('File already exists')
        return super().clean()
    
    def save(self, *args, **kwargs):
        # Fix this function and clean media folder
        self.name = self.name.capitalize()
        # self.picture.path = f"{settings.MEDIA_ROOT}/{os.path.basename(str(self.picture))}"
        # print(self.picture, self.picture.path)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})
