/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/recipe_manager/*.html", "./recipes/templates/recipes/*.html"],
  theme: {
    extend: {
      fontFamily: {
        'roboto': ['"Roboto Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}

