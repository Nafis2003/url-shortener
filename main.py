from fastapi import FastAPI
from fastapi.responses import RedirectResponse,JSONResponse
import os
from dotenv import load_dotenv
from tortoise import Tortoise, fields
from tortoise.models import Model
from contextlib import asynccontextmanager
from models import URL
from uuid_extensions import uuid7
import base64

load_dotenv()
connection_string = os.getenv("DATABASE_URL")
base_url = os.getenv("BASE_URL")

@asynccontextmanager
async def lifespan(app):
    await Tortoise.init(
        db_url=connection_string,
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

app = FastAPI(title="URL Shortener",version="1.0.1",description="A URL shortening service",lifespan=lifespan)

@app.get("/",status_code=200)
async def root():
    return {"author": "Nafis Sadiq","version": "1.0.1","description": "A URL shortening service","api-docs":f"{base_url}/docs","github": "https://github.com/Nafis2003"}

def generate_short_id():
    uuid_bytes = uuid7().bytes
    return base64.urlsafe_b64encode(uuid_bytes)[:8].decode().rstrip("=")

@app.post("/short")
async def short(url: str):
    if not url:
        return JSONResponse(content={"status": "error", "message": "URL is required"}, status_code=400)
    try:
        short_url = base_url + "/" + generate_short_id()
        resp = await URL.create(url=url, short_url=short_url)
        return JSONResponse(content={"status": "success", "data": resp.to_json()}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": "Failed to create short URL"}, status_code=500)

@app.get("/{short_id}")
async def redirect(short_id: str):
    url= await URL.filter(short_url=base_url + "/" + short_id)
    if url:
        return RedirectResponse(url=url[0].url)
    return JSONResponse(content={"status": "error", "message": "Invalid short URL"}, status_code=404)

