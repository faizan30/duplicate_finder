from typing import Union, List, Dict
import os
import uuid

from fastapi import FastAPI
from src.duplicate_finder import find_duplicates, set_retriever, ranker
from src.vector_data_manager import write_documents
from src.vector_data_manager import load_document_store
import json

# DOCUMENT STORE INITIALIZATION
document_store_dir = ".data/document_store/"
index_name = "new_faiss_index.faiss"
database_name = "faiss_document_store.db"

global document_store_global
document_store_global = load_document_store(document_store_dir, index_name, database_name)

global retriever_global 
retriever_global = set_retriever(document_store_global)


# FASTAPI INITIALIZATION
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "This is Home Page of Duplicate Ranker API"}


@app.post("/duplicates")
def get_duplicates(title:str, content:str, retriever_k=10, ranker_k=5):
    text = title+"\n"+content
    return find_duplicates(text, retriever_global, ranker, int(retriever_k), int(ranker_k))


@app.post("/write_document")
def write_documents_api(title:str, content:str):
    # document_store = load_document_store(document_store_dir, index_name)
    doc = {}
    doc['content'] = title+"\n"+content
    doc['meta'] = {'meta': {'name': title, 'id': str(uuid.uuid4())}}
    
    write_documents([doc], document_store_global, retriever_global)
    index_path = document_store_dir+index_name
    document_store_global.save(index_path=index_path)

    return {"status": "success"}


@app.get("/docstore_info")
def docstore_info_api():
    vector_document_store = load_document_store(document_store_dir, index_name)
    count = vector_document_store.get_document_count()
    return {"idea_count": count}

# @app.post("/duplicates_batch")
# def get_duplicates_batch(text_list:List[dict], retriever_k=10, ranker_k=5):
#     text_batch = []
#     for text_dict in text_list:
#         text = text_dict["title"]+"\n"+text_dict["content"]
#         text_batch.append(text)
#     return find_duplicates_batch(text_batch, retriever_k, ranker_k)
    
# if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=9800)

    # # WRITE DOCUMENTS TO THE DOCUMENT STORE INITIALLY
    # from src.vector_data_manager import prepare_documents, write_documents
    # data_path = ".data/AI Sample Data.xlsx"
    # documents = prepare_documents(data_path)
    # document_store_dir = ".data/document_store/"
    # index_name = "new_faiss_index.faiss"
    # index_path = document_store_dir+index_name
    # # #write documents to the document store
    # write_documents(documents, document_store_global, retriever_global)
    # document_store_global.save(index_path=index_path)

    # #COUNT DOCUMENTS
    # count = document_store.get_document_count()
    # print("The number of documents: ", count)

    # dummy_data = [
    #     {
    #         'title': 'Vehicle Information Display Panel',
    #         'content':"A display panel at Fleet front desk offers vehicle updates to the users. Users can input equipment ID, plate number, cost center, or coordinator's PR number to determine the job status and ascertain if the vehicle is awaiting further action or if it is prepared for use."
    #     }
    # ]