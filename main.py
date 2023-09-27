from typing import Union, List, Dict
import os

from fastapi import FastAPI
from src.duplicate_finder import find_duplicates
from src.vector_data_manager import write_documents
from src.vector_data_manager import load_document_store
import json


document_store_dir = ".data/document_store/"
index_name = "new_faiss_index.faiss"
database_name = "faiss_document_store.db"
document_store = load_document_store(document_store_dir, index_name, database_name)

model_format = "retribert"
embedding_model = "yjernite/retribert-base-uncased"
# embedding_model = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
# model_format = "sentence_transformers"
from haystack.nodes import EmbeddingRetriever
retriever = EmbeddingRetriever(document_store=document_store,
                            embedding_model=embedding_model,
                            model_format=model_format)

from haystack.nodes import BM25Retriever, SentenceTransformersRanker
ranker_model = "cross-encoder/ms-marco-MiniLM-L-12-v2"
ranker = SentenceTransformersRanker(model_name_or_path=ranker_model)

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "This is Home Page of Duplicate Ranker API"}


@app.post("/duplicates")
def get_duplicates(title:str, content:str, retriever_k=10, ranker_k=5):
    
    text = title+"\n"+content
    return find_duplicates(text, retriever, ranker, int(retriever_k), int(ranker_k))


@app.post("/write_documents")
def write_documents_api(text_list:List[dict]):
    writer_document_store = load_document_store(document_store_dir, index_name_global)
    write_documents(text_list, writer_document_store, retriever)
    index_path = document_store_dir+index_name_global
    document_store.save(index_path=index_path)
    return {"status": "success"}


@app.get("/docstore_info")
def docstore_info_api(text_list:List[dict]):
    vector_document_store = load_document_store(document_store_dir, index_name_global)
    count = document_store.get_document_count()
    return {"document_count": "count"}

# @app.post("/duplicates_batch")
# def get_duplicates_batch(text_list:List[dict], retriever_k=10, ranker_k=5):
#     text_batch = []
#     for text_dict in text_list:
#         text = text_dict["title"]+"\n"+text_dict["content"]
#         text_batch.append(text)
#     return find_duplicates_batch(text_batch, retriever_k, ranker_k)
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9800)
    # from src.vector_data_manager import prepare_documents, write_documents

#     # WRITE DOCUMENTS TO THE DOCUMENT STORE
#     data_path = ".data/AI Sample Data.xlsx"
#     documents = prepare_documents(data_path)
#     document_store_dir = ".data/document_store/"
#     index_name = "new_faiss_index.faiss"
#     index_path = document_store_dir+index_name
#     # #write documents to the document store
#     write_documents(documents, document_store, retriever)
#     document_store.save(index_path=index_path)

#     #COUNT DOCUMENTS
#     count = document_store.get_document_count()
#     print("The count of the documents: ", count)

    # [
    #     {
    #         'title': 'Vehicle Information Display Panel',
    #         'content':"A display panel at Fleet front desk offers vehicle updates to the users. Users can input equipment ID, plate number, cost center, or coordinator's PR number to determine the job status and ascertain if the vehicle is awaiting further action or if it is prepared for use."
    #     }
    # ]

    