
from typing import List, Optional, Union

from pydantic import BaseModel


class Ingredient(BaseModel):
    item: Optional[str] = None
    quantity: Optional[Union[float, str]] = None
    unit: Optional[str] = None

    def __str__(self):
        if self.quantity is None:
            return self.item
        if self.unit is None:
            return f"{self.item} {self.quantity}"
        return f"{self.item} {self.quantity} {self.unit}"

class Recipe(BaseModel):
    id: int
    title: Optional[str] = None
    page: Optional[int] = None
    author: Optional[str] = None
    ingredients: Optional[List[Ingredient]] = None
    instructions: Optional[List[str]] = None

    @property
    def number_of_ingredients(self):
        if self.ingredients is None:
            return 0
        return len(self.ingredients)

    @property
    def number_of_steps(self):
        if self.instructions is None:
            return 0
        return len(self.instructions)

    @property
    def ingredients_text(self):
        return "\n".join([str(ingredient) for ingredient in self.ingredients])

    @property
    def ingredient_items_text(self):
        return ",".join([ingredient.item for ingredient in self.ingredients])

    @property
    def steps_text(self):
        return "\n".join([f"{i+1}. {step}" for i, step in enumerate(self.instructions)])

    @property
    def text(self):
        return f"{self.title}\n\ningredients:\n{self.ingredients_text}\n\nsteps:\n{self.steps_text}"

    @property
    def main_image_filename(self):
        return f"main_{self.id}.png"

    def get_step_image_filename(self, n):
        return f"r{self.id}_s{n}.png"


class CookBook(BaseModel):
    recipes: List[Recipe]
