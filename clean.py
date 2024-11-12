from settings import STRUCTURED_RECIPES_FILEPATH, ID_STRUCTURED_RECIPES_FILEPATH,  OK_STRUCTURED_RECIPES_FILEPATH
import json
from loguru import logger
from typing import Dict

def is_missing_fields(d: Dict):
    if not d.get("title"):
        logger.warning(f"Title is missing in {d}")
        return True
    if not d.get("ingredients"):
        logger.warning(f"Ingredients is missing in {d}")
        return True
    if not d.get("instructions"):
        logger.warning(f"Instructions is missing in {d}")
        return True

def validate():
    with open(STRUCTURED_RECIPES_FILEPATH, "r") as f:
        data = json.load(f)
        for d in data:
            if is_missing_fields(d):
                logger.warning(f"Validation failed for {d}")

def add_id():
    with open(STRUCTURED_RECIPES_FILEPATH, "r") as f:
        data = json.load(f)
        for i, d in enumerate(data):
            d["id"] = i
        with open(ID_STRUCTURED_RECIPES_FILEPATH, "w") as f:
            json.dump(data, f, indent=4)

def select_ok_recipes(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)
        ok_recipes =  [d for d in data if not is_missing_fields(d)]
        logger.info(f"Number of recipes: {len(data)}")
        logger.info(f"Number of OK recipes: {len(ok_recipes)}")
        logger.info(f"Number of dubious recipes: {len(data) - len(ok_recipes)}")
        logger.info(f"percentage of dubious recipes: {(1-len(ok_recipes) / len(data)) * 100:.2f}%")
        logger.info(f"Saving OK recipes to {output_file}")
        with open(output_file, "w") as f:
            json.dump(ok_recipes, f, indent=4)

if __name__ == "__main__":
    add_id()
    select_ok_recipes(ID_STRUCTURED_RECIPES_FILEPATH, OK_STRUCTURED_RECIPES_FILEPATH)
