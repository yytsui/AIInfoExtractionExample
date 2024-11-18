import json
import os

from dotenv import load_dotenv
from icecream import ic
from loguru import logger
from openai import OpenAI

from model import CookBook
from pdf_text import read_pdf
from settings import FILE_PATH, SYSTEM_CONTENT, DEBUG, STRUCTURED_RECIPES_FILEPATH, \
    STRUCTURED_NO_RECIPES_WARNINGS_FILEPATH
from utils import dump_json

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def find_structured_info_with_ai(prompt, system_content, response_format):
    completion = openai_client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system",
             "content": system_content
            },
            {
                "role": "user",
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
            f"There are pages without any recipe.\n" 
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

        if DEBUG and len(recipes) > 5:
            ic(recipes)
            logger.info("here")
            break
    logger.info(f"extraction done.number of recipes found: {len(recipes)}, ready to persist to file.")
    recipes_dict = [recipe.model_dump() for recipe in recipes]

    dump_json(recipes_dict, STRUCTURED_RECIPES_FILEPATH)
    dump_json(no_recipes_warnings, STRUCTURED_NO_RECIPES_WARNINGS_FILEPATH)



if __name__ == "__main__":
    main()