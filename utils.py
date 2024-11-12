import json
from pathlib import Path
from loguru import logger


def dump_json(data, file_path):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Dumping data to {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)