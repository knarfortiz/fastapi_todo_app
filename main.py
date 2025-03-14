from typing import Union

from fastapi import FastAPI

import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
