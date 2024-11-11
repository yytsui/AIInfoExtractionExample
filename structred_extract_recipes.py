import json

from loguru import logger

from dotenv import load_dotenv
import os
from openai import OpenAI
from icecream import ic
from model import CookBook, Recipe
from pdf_text import read_pdf
from loguru import logger

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FILE_PATH = "data/originalrecipeso00orde.pdf"
SYSTEM_CONTENT = "You are a helpful information extraction assistant. You will extract recipes from a book."

def find_structured_info_with_ai(prompt, system_content, response_format):
    completion = openai_client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system",
             #"content": "You are a helpful information extraction assistant. You will extract recipes from a book."
             "content": system_content
            },
            {
                "role": "user",
                #"content": f"find the agreement title, date, entity which has the agreement with Novus and subject property in this agreement : {agreement.content_text}",
                "content": prompt
            },
        ],
        response_format=response_format,
    )
    message = completion.choices[0].message
    if message.parsed:
        ic(message.parsed)
        return message.parsed
    else:
        ic(message.refusal)
        return message.refusal

def generate_prompt(page_number, text):
    return (f"Extract all recipes from the following text starting from ---Page {page_number}--- "
            f"Each recipe should include: - title - Ingredients (with item, quantity, and unit) - "
            f"Instructions (use the original text as much as possible) - Author - Page number\n" 
            f" There could be multiple recipes in a page, return a list of recipes in the page. "
            f" Not every page will have a recipe\n" 
            f"---Page {page_number}--\n{text}")

def main():
    content = read_pdf(FILE_PATH)
    recipes = []
    no_recipes_warnings = []
    for page_number, text in content.items():
        prompt = generate_prompt(page_number, text)
        response = find_structured_info_with_ai(prompt, SYSTEM_CONTENT, CookBook)
        if isinstance(response, CookBook) and response.recipes:
            recipes.extend(response.recipes)
            logger.info(f"number of recipes found in page {page_number}: {len(response.recipes)}")
        else:
            d = dict(page_number=page_number, warning=f"no recipe in this page: {response}",
                                           page_content=text)
            logger.warning(d)
            no_recipes_warnings.append(d)

        if len(recipes) > 5:
            ic(recipes)
            logger.info("here")
            break
    recipes_dict = [recipe.model_dump() for recipe in recipes]
    with open("gen_results/structed_recipes.json", "w", encoding="utf-8") as f:
        json.dump(recipes_dict, f, indent=4)
    with open("gen_results/no_recipes_warnings.json", "w", encoding="utf-8") as f:
        json.dump(no_recipes_warnings, f, indent=4)



if __name__ == "__main__":
    main()