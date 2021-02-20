from dotenv import load_dotenv
# load environment variables at app start
load_dotenv()

import os

import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from users import user_router

DATABASE_URL = os.environ["DATABASE_URL"]

app = FastAPI()

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["users.models"]},
    generate_schemas=True,
)

app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run(app)
