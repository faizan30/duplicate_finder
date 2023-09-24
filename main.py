from typing import Union

from fastapi import FastAPI
from src.duplicate_finder import find_duplicate
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.post("/duplicate")
def get_duplicates(text, threshold):
    return find_duplicate(text, threshold)

@app.get("/duplicate")
def get_duplicates(text="", threshold=0.7):
    return find_duplicate(text, threshold)
    