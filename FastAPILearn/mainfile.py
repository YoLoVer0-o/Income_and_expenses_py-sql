from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated
import jwt

app = FastAPI()

# MongoDB connection
db_connection = MongoClient("mongodb://localhost:27017/")
db = db_connection["users"]
collection = db["users"]

# Security utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT Configuration
SECRET_KEY = "707eb0c8d124fe8cd616aa56fe08732a01ede801e1f01ce1354b33c5f5944a93"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

for user in collection.find():
    plain_password = user["password"]  # Assuming it's plain text
    if not plain_password.startswith("$2b$"):  # bcrypt hashes start with $2b$
        hashed_password = pwd_context.hash(plain_password)
        collection.update_one(
            {"_id": user["_id"]}, {"$set": {"password": hashed_password}}
        )
        print(f"Updated password for user: {user['username']}")

# Pydantic model for user input
class Users(BaseModel):
    username: str
    password: str


# Utility to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Utility to hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# Utility to authenticate user using MongoDB
def authenticate_user(username: str, password: str):
    user = collection.find_one({"username": username})
    if user is None or not verify_password(password, user["password"]):
        return None
    return user


# Utility to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Root route
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Token generation endpoint (Login)
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Dependency to get the current user from the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user


# Protected route
@app.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "full_name": current_user.get("full_name", ""),
    }


# Create user endpoint
@app.post("/users/", tags=["user"])
async def create_user(users: Users):
    hashed_password = get_password_hash(users.password)
    user_data = {"username": users.username, "password": hashed_password}
    result = collection.insert_one(user_data)
    return {"id": str(result.inserted_id), "username": users.username}


# Get user by ID
@app.get("/users/user_id?{user_id}", tags=["user"])
async def get_user(user_id: str ):
    user_info = collection.find_one({"_id": ObjectId(user_id)})
    if user_info:
        return {
            "user_id": str(user_info["_id"]),
            "username": user_info["username"],
        }
    else:
        raise HTTPException(status_code=404, detail="User Not Found")


# Update user
@app.put("/users/{user_id}", tags=["user"])
async def update_user(user_id: str, update_data: Users):
    update_info = {"username": update_data.username}
    if update_data.password:
        update_info["password"] = get_password_hash(update_data.password)
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_info})
    if result.modified_count == 1:
        return {"id": user_id, "username": update_data.username}
    else:
        raise HTTPException(status_code=404, detail="User Not Found")


# Partially update user
@app.patch("/users/{user_id}", tags=["user"])
async def patch_user(user_id: str, update_data: Users):
    update_info = {"username": update_data.username}
    if update_data.password:
        update_info["password"] = get_password_hash(update_data.password)
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_info})
    if result.modified_count == 1:
        return {"id": user_id, "username": update_data.username}
    else:
        raise HTTPException(status_code=404, detail="User Not Found")


# Delete user
@app.delete("/users/{user_id}", tags=["user"])
async def delete_user(user_id: str):
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"status": "Delete Success"}
    else:
        raise HTTPException(status_code=404, detail="User Not Found")
