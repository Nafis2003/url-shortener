from fastapi import FastAPI
from fastapi.responses import RedirectResponse
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

app = FastAPI(lifespan=lifespan)

def generate_short_id():
    uuid_bytes = uuid7().bytes
    return base64.urlsafe_b64encode(uuid_bytes)[:8].decode().rstrip("=")

@app.post("/short")
async def short(url: str):
    short_url = base_url + "/" + generate_short_id()
    resp = await URL.create(url=url, short_url=short_url)
    return {"status": "success", "data": resp.to_json()}

@app.get("/{short_id}")
async def redirect(short_id: str):
    url= await URL.filter(short_url=base_url + "/" + short_id)
    if url:
        return RedirectResponse(url=url[0].url)
    return {"status": "error", "message": "URL not found"}

