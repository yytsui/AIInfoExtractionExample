import json
import os
from logging import warning
from typing import Dict
from string import Template

import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger

load_dotenv()
# Set your OpenAI API Key
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
FILE_PATH = "data/originalrecipeso00orde.pdf"
prompt_template =  Template("""
    Extract all recipes from the following text starting from ---Page $page_number---. Each recipe should include:
    - Recipe name
    - Ingredients (with item, quantity, and unit)
    - Instructions (use the original text as much as possible)
    - Author
    - Page number

    Format each recipe in JSON format like this:

    {{
        "recipe": "Recipe Name",
        "page": {page_number},
        "author": "Author Name",
        "ingredients": [
            {{"item": "ingredient 1", "quantity": 2, "unit": "cups"}},
            {{"item": "ingredient 2", "quantity": 1, "unit": "tablespoon"}}
        ],
        "instructions": [
            "Step 1",
            "Step 2",
            "Step 3"
        ]
    }}.
    There could be multiple recipes in a page, return a list of recipes in the page.
    Not every page will have a recipe, in case there is no recipes in the page, return a json like this 
    {{
       "warning": "no recipe in this page",
        "page": $page_number
    }}
    
    ---Page $page_number---
    $text
    """)
SYSTEM_CONTENT = "You are a helpful information extraction assistant. You will extract recipes from a book."


def save_recipes_to_json(recipes_text, output_file):
    """
    Save extracted recipes to a JSON file.
    """
    try:
        recipes = json.loads(recipes_text)
        with open(output_file, 'w') as f:
            json.dump(recipes, f, indent=4)
        print(f"Recipes have been saved to {output_file}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")



def ask_ai(prompt, system_content=SYSTEM_CONTENT):

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system",
             "content": system_content},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    return content

def read_pdf(pdf_path: str) -> Dict:
    """Extract text from PDF file."""
    page_text = {}
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(pdf_reader.pages):
                page_text[i+1] = page.extract_text()
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        page_text = {"error": f"Error reading PDF: {e}"}
    return page_text

def run():
    content = read_pdf(FILE_PATH)
    results = []
    warnings = []
    for page_number, text in content.items():
        prompt = prompt_template.substitute(page_number=page_number,text=text)
        logger.info(prompt)
        text_response = ask_ai(prompt)
        response = text_response.split("```json")[1].split("```")[0]
        logger.info(response)

        result = json.loads(response)
        if "warning" in result:
            logger.warning(result)
            warnings.append(result)
        else:
            logger.info(result)
            logger.info(f"Extracted {len(result)} recipes from page {page_number}")
            results += result
    #print(content)
    #print(len(content))
    with open("recipes.json", "w") as f:
        json.dump(results, f, indent=4)
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)
if __name__ == "__main__":
    run()
