from model import Ingredient, Recipe
from typing import List
import json
from settings import OK_STRUCTURED_RECIPES_FILEPATH

def format_ingredients_table(ingredients: List[Ingredient]) -> str:
    """Generate a 3-column markdown table for ingredients"""
    table = "| Ingredient | Quantity | Unit |\n"
    table += "|------------|----------|------|\n"

    for ing in ingredients:
        item = ing.item if ing.item else ''
        quantity = str(ing.quantity) if ing.quantity is not None else ''
        unit = ing.unit if ing.unit else ''
        table += f"| {item} | {quantity} | {unit} |\n"

    return table

def generate_recipe_markdown(recipe: Recipe) -> str:
    """Generate markdown for a recipe with available images"""

    markdown = f"# {recipe.title}\n\n"

    # Add main image if available with width 800px
    main_image = f"/notes/assets/image/{recipe.main_image_filename}"
    markdown += f"<img src='{main_image}' width='800px'/>\n\n"

    # Add ingredients section with table
    markdown += "## Ingredients\n\n"
    markdown += format_ingredients_table(recipe.ingredients)
    markdown += "\n"

    # Add instructions with images at half size (400px)
    markdown += "## Instructions\n\n"
    for i, step in enumerate(recipe.instructions):
        markdown += f"{i+1}. {step}\n"
        step_image = f"/notes/assets/image/{recipe.get_step_image_filename(i)}"
        markdown += f"\n\t<img src='{step_image}' width='400px'/>\n\n"

    # Add footer with author and page
    markdown += "\n---\n"
    if recipe.author:
        markdown += f"*Recipe by: {recipe.author}*"
    if recipe.page:
        markdown += "\n\n"
        markdown += f" • *Source: [Original Recipes of Good Things to Eat](https://ia601303.us.archive.org/34/items/originalrecipeso00orde/originalrecipeso00orde.pdf) page {recipe.page}*"

    return markdown

def generate_cookbook_markdown(recipes: List[Recipe], available_files: List[str]) -> str:
    """Generate markdown for entire cookbook"""
    # Add image/ prefix to all file paths in available_files
    available_files = [f"image/{f}" for f in available_files]

    markdown = "# Recipe Book\n\n"
    markdown += "## Table of Contents\n\n"

    # Generate TOC
    for recipe in recipes:
        markdown += f"- [{recipe.title}](#{recipe.title.lower().replace(' ', '-')})\n"

    markdown += "\n---\n\n"

    # Generate each recipe
    for recipe in recipes:
        markdown += generate_recipe_markdown(recipe, available_files)
        markdown += "\n\n---\n\n"

    return markdown

def save_markdown(recipes: List[Recipe], available_files: List[str], output_file: str):
    markdown = generate_cookbook_markdown(recipes, available_files)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

def main():
    # Load recipes from file
    recipes = []
    sample_recipe_ids = (117, 294, 32, 445, 61)
    with open(OK_STRUCTURED_RECIPES_FILEPATH ,'r', encoding='utf-8') as f:
        recipes = [Recipe(**r) for r in json.load(f)]
    sample_recipes = [r for r in recipes if r.id in sample_recipe_ids]
    # Load image files from image directory
    for recipe in sample_recipes:
        markdown = generate_recipe_markdown(recipe)
        with open(f"gen_recipes_markdown/r{recipe.id}.md", 'w', encoding='utf-8') as f:
            f.write(markdown)

if __name__ == "__main__":
    main()