def convert_recipe(recipe) -> dict:
    base_url = "http://127.0.0.1:8000"
    image_url = f"{base_url}/images/{recipe['image']}" if "image" in recipe else None
    return {
        "id": str(recipe["_id"]),
        "name": recipe["name"],
        "ingredients": recipe["ingredients"],
        "calories": recipe["calories"],
        "weight": recipe["weight"],
        "description": recipe["description"],
        "favorite": recipe["favorite"],
        "cooking": recipe["cooking"],
        "image": image_url,
    }

def convert_recipes(recipes) -> list:
    return [convert_recipe(recipe) for recipe in recipes]