# Recipe Manager
## Django note app for recipes

![screenshot of the app](/media/recipe_manager_screenshot.png)

### Description

This project is a recipe note app using **Django** as Back-End, which used the Model, View, Template architecture. I developed it as a practice Django project and styled it using **Tailwind CSS** diretcly on the Django Templates.

### Features

The user is able to Create, Retrieve, Update and Delete recipes with basic data fields such as ingredients, instructions or tags. It's meant as a notes app more than a blog, as it does not implement User login.

The website also includes a search bar that can look for recipes based on their name of tags.

## CI/CD


### Testing

The project was tested using the Django Test classes, extending the *unittest* Python module.
This is further integrated within a Django **GitHub Workflow** testing the project on each push.

### Docker

This website is not deployed but a Docker Image has been added to this repo and a package made out of it (see [packages](https://github.com/LucasPages/Recipe-manager/pkgs/container/recipe_manager%2Frecipe_app)) made available. A GitHub workflow builds the image and package on every push. You can pull the package to easily test the website : 
```console
$ docker pull ghcr.io/lucaspages/recipe_manager/recipe_app:latest
```


*Thank you for looking at this repo !*