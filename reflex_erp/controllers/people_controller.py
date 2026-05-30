import reflex as rx
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from reflex_erp.db import collection

# Create a FastAPI app with authentication
fastapi_app = FastAPI(title="Secure API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@fastapi_app.get("/api/people")
async def get_items():
    return [
        {**item, "_id": str(item["_id"])}
        for item in collection.find()
    ]

# Add a protected route
@fastapi_app.get("/api/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return dict(message="This is a protected endpoint")


# Create a token endpoint
@fastapi_app.post("/token")
async def login(username: str, password: str):
    # In a real app, you would validate credentials
    if username == "user" and password == "password":
        return dict(access_token="example_token", token_type="bearer")
    return dict(error="Invalid credentials")


