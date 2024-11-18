from settings import OK_STRUCTURED_RECIPES_FILEPATH
import json
from typing import List, Dict
from model import Recipe
from loguru import logger
import random
from icecream import ic


def load_all_recipes(json_file=OK_STRUCTURED_RECIPES_FILEPATH) -> List[Recipe]:
    with open(json_file, "r") as f:
        data = json.load(f)
        recipes = [Recipe(**d) for d in data]
    return recipes

def fetch_recipe_samples(size=10, min_ingredients=5, min_steps=4) -> List[Recipe]:
    random.seed(1)
    recipes = load_all_recipes()
    recipes = [r for r in recipes if min_ingredients <= r.number_of_ingredients and
               min_steps <= r.number_of_steps]
    logger.info(f"Number of recipes with at least {min_ingredients} ingredients and {min_steps} steps: {len(recipes)}")
    return random.sample(recipes, size)

def main():
    #recipes = load_all_recipes()
    #logger.info(f"Number of total recipes: {len(recipes)}")
    samples = fetch_recipe_samples(5)
    ic(samples)
    return
    for r in samples:
        logger.info(r.text)
        logger.info("-" * 80)

if __name__ == "__main__":
    main()