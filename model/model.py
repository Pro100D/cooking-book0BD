from typing import Optional

from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    calories: int
    weight: int
    description: str
    favorite: bool
    image: Optional[str] = None
    cooking: str