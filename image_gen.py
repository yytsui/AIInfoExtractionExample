from openai import OpenAI
from load_recipes import fetch_recipe_samples
from dotenv import load_dotenv
import os
from loguru import logger
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt):
    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )

    image_url = response.data[0].url
    return image_url

def main():
    recipe = fetch_recipe_samples(1)[0]
    #prompt = f"A {recipe.title} which was made from ingredients: {recipe.ingredient_items_text}."
    #prompt = f"step by step instructions\n{recipe.steps_text}\n to make {recipe.title}"
    for step in recipe.instructions:
        prompt = f"{step}"
        logger.info(f"generating image prompt: {prompt}")
        image_url = generate_image(prompt)
        print(image_url)


if __name__ == "__main__":
    main()
