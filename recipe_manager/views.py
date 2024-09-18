from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "recipe_manager/index.html"