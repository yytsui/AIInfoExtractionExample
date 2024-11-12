from loguru import logger
from ai import ask_ai
from settings import OK_STRUCTURED_RECIPES_FILEPATH, CH_RECIPES_FILEPATH
import json
from utils import load_openai_json, dump_json

def translate_json(json_data):
    system_content = "You are a helpful translation assistant. You will translate a JSON data."
    prompt = (f"Translate the following JSON data to Traditional Chinese, only translate value, "
              f"keep key unchanged in English.\n"
              f"Keep the author name in English.\n"
              f"```json\n"
              f"{json_data}```")
    response = ask_ai(prompt, system_content)
    return response

def main():
    ch_recipes = []
    with open(OK_STRUCTURED_RECIPES_FILEPATH, "r") as f:
        data = json.load(f)
        for d in data:
            logger.info(f"Translating {d}")
            response = translate_json(json.dumps(d, indent=4))
            new_d = load_openai_json(response)
            logger.info(f"Translated result: {new_d}")
            if new_d:
                ch_recipes.append(new_d)
            else:
                logger.error(f"Error translating {d}")

    logger.info(f"Number of translated recipes: {len(ch_recipes)}")
    logger.info(f"Saving translated recipes to {CH_RECIPES_FILEPATH}")
    dump_json(ch_recipes, CH_RECIPES_FILEPATH)



if __name__ == "__main__":
    main()



