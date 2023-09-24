from typing import Union

from fastapi import FastAPI
from src.duplicate_finder import find_duplicate
from src.vector_data_manager import write_documents
from src.vector_data_manager import load_document_store
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

@app.get("/write_documents")
def get_duplicates(text_list=[]):
    index_path = "document_store/my_faiss_index.faiss"
    document_store = load_document_store(index_path)
    return write_documents(text_list, document_store)
    