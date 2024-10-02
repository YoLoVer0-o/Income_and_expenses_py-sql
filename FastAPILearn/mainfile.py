from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId

app = FastAPI()
db_connection = MongoClient("mongodb://localhost:27017/")
db = db_connection["users"]
collection = db["users"]


class Users(BaseModel):
    username: str
    password: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Post Request
@app.post("/users/")
async def create_user(users: Users):
    result = collection.insert_one(users.dict())
    return {
        "id": str(result.inserted_id),
        "username": users.username,
        "password": users.password,
    }


# Get Request
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user_info = collection.find_one({"_id": ObjectId(user_id)})
    if user_info:
        return {
            "user_id": str(user_info["_id"]),
            "username": user_info["username"],
            "password": user_info["password"],
        }
    else:
        raise HTTPException(status_code=404, detail="User Not Found")


# Update Request
@app.put("/users/{user_id}")
async def user_update(user_id: str, update_data: Users):
    result = collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update_data.dict(exclude_unset=True)}
    )
    if result.modified_count == 1:
        return {
            "id": user_id,
            "username": update_data.username,
            "password": update_data.password,
        }
    else:
        raise HTTPException(status_code=404, detail="User Not Found")


# Patch Request
@app.patch("/users/{user_id}")
async def user_update_patch(user_id: str, update_data: Users):
    result = collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update_data.dict(exclude_unset=True)}
    )
    if result.modified_count == 1:
        return {
            "id": user_id,
            "username": update_data.username,
            "password": update_data.password,
        }
    else:
        raise HTTPException(status_code=404, detail="User Not Found")


# Delete Requset
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"status": "Delete Success"}
    else:
        raise HTTPException(status_code="404", detail="User Not Found")
