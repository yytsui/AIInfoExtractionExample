import json
from pathlib import Path
from loguru import logger


def dump_json(data, file_path):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Dumping data to {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf-8-not-as-a-u-escape-sequence
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_openai_json(response):
    try:
        d = json.loads(response.split("```json")[1].split("```")[0])
        return d
    except Exception as e:
        logger.error(f"Error loading json: {e}")
        return None