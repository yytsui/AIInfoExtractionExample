import json
import uuid

from sqlite_utils import Database

from model import Recipe
from settings import OK_STRUCTURED_RECIPES_FILEPATH


def get_uuid():
    return str(uuid.uuid4())

def make_db_dict(recipe: Recipe):
    return dict(id=recipe.id, title=recipe.title, page=recipe.page, author=recipe.author)


def make_ingredients_db_dict(recipe: Recipe):
    return [dict(recipe_id=recipe.id, item=ingredient.item, quantity=ingredient.quantity,
                 unit=ingredient.unit, id=get_uuid())
            for ingredient in recipe.ingredients]


def make_instructions_db_dict(recipe: Recipe):
    return [dict(recipe_id=recipe.id, order=i,instruction=instruction, id=get_uuid())
            for i, instruction in enumerate(recipe.instructions)]


def json2sqlite(json_file, sqlite_file):
    with open(json_file) as f:
        data = json.load(f)
    db = Database(sqlite_file)
    recipes = [Recipe(**recipe) for recipe in data]
    db["recipes"].insert_all([make_db_dict(recipe) for recipe in recipes], pk="id")
    db["ingredients"].insert_all([ingredient for recipe in recipes
                                  for ingredient in make_ingredients_db_dict(recipe)],
                                 foreign_keys=[("recipe_id", "recipes", "id")], pk="id")
    db["instructions"].insert_all([instruction for recipe in recipes
                                   for instruction in make_instructions_db_dict(recipe)],
                                  foreign_keys=[("recipe_id", "recipes", "id")], pk="id")


if __name__ == "__main__":
    json2sqlite(OK_STRUCTURED_RECIPES_FILEPATH, "data/recipes1.db")