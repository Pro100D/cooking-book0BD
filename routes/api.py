from bson import ObjectId
from fastapi import APIRouter, HTTPException
import os
import base64

from starlette.responses import JSONResponse

from config.config import recipe_collections
from model.model import Recipe
from serializer.serializer import convert_recipe, convert_recipes

endPoints = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@endPoints.get('/recipes')
def get_recipes():
    recipes = recipe_collections.find()
    converted_recipes = convert_recipes(recipes)
    return { "Status": "Ok", "data": converted_recipes }
@endPoints.get('/recipes/favorite')
def get_recipe():
    recipes = recipe_collections.find({'favorite': True})
    converted_recipe = convert_recipes(recipes)
    return {"Status": "Ok", "data": converted_recipe}

@endPoints.post("/recipes")
async def create_recipe(recipe: Recipe):
    try:
        image_data = base64.b64decode(recipe.image)
        image_filename = f"{ObjectId()}.jpg"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as image_file:
            image_file.write(image_data)

        recipe_data = recipe.dict()
        recipe_data["image"] = image_filename
        result = recipe_collections.insert_one(recipe_data)

        recipe_data["_id"] = result.inserted_id
        return JSONResponse(content=convert_recipe(recipe_data), status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@endPoints.patch('/recipes/{id}')
def update_recipe(id: str, updated_recipe: Recipe):
    try:
        recipe = recipe_collections.find_one({"_id": ObjectId(id)})
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        if updated_recipe.image:
            old_image_filename = recipe.get("image")
            if old_image_filename:
                old_image_path = os.path.join(UPLOAD_DIR, old_image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            new_image_data = base64.b64decode(updated_recipe.image)
            new_image_filename = f"{ObjectId()}.jpg"
            new_image_path = os.path.join(UPLOAD_DIR, new_image_filename)
            with open(new_image_path, "wb") as image_file:
                image_file.write(new_image_data)

            updated_recipe.image = new_image_filename

        update_dict = updated_recipe.dict(exclude_unset=True)
        if "image" in update_dict:
            update_dict["image"] = updated_recipe.image

        result = recipe_collections.update_one(
            {"_id": ObjectId(id)}, {"$set": update_dict}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update recipe")

        updated_recipe = recipe_collections.find_one({"_id": ObjectId(id)})
        return JSONResponse(content=convert_recipe(updated_recipe), status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating recipe: {e}")

@endPoints.delete('/recipes/{id}')
def delete_recipe(id: str):
    try:
        recipe = recipe_collections.find_one({"_id": ObjectId(id)})
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        image_filename = recipe.get("image")
        if image_filename:
            image_path = os.path.join(UPLOAD_DIR, image_filename)

            if os.path.exists(image_path):
                os.remove(image_path)

        recipe = recipe_collections.find_one({"_id": ObjectId(id)})
        result = recipe_collections.delete_one({"_id": ObjectId(id)})

        convertedRecipe = convert_recipe(recipe)
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete recipe")

        return {"detail": "Recipe deleted successfully", "data": convertedRecipe}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting recipe: {e}")