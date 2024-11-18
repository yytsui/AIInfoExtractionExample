from openai import OpenAI
from load_recipes import fetch_recipe_samples
from dotenv import load_dotenv
import os
from loguru import logger
import urllib.request
from settings import IMAGE_STORAGE_PATH
from pathlib import Path
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt):
    logger.info(f"generating image prompt: {prompt}")
    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    image_url = response.data[0].url
    return image_url

def generate_main_image_from_recipe(recipe):
    prompt = f"A {recipe.title} which was made from ingredients: {recipe.ingredient_items_text}."
    image_url = generate_image(prompt)
    return image_url

def generate_image_from_step(step):
    image_url = generate_image(step)
    return image_url

def persist_image(image_url, filepath):
    logger.info(f"Downloading image from {image_url} to {filepath}")
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(image_url, filepath)

def generate_recipe_images_and_persist(recipe):
    #def main():
    #recipe = fetch_recipe_samples(1)[0]
    logger.info(f"Generating images for recipe: {recipe.title} {recipe.id}")
    img_url = generate_main_image_from_recipe(recipe)
    main_image_filepath = os.path.join(IMAGE_STORAGE_PATH, recipe.main_image_filename)
    persist_image(img_url, main_image_filepath)
    for i, step in enumerate(recipe.instructions):
        step_image_url = generate_image_from_step(step)
        step_image_filepath = os.path.join(IMAGE_STORAGE_PATH, recipe.get_step_image_filename(i))
        persist_image(step_image_url, step_image_filepath)

def main():
    recipes = fetch_recipe_samples(5)
    for recipe in recipes:
        generate_recipe_images_and_persist(recipe)

if __name__ == "__main__":
    main()
