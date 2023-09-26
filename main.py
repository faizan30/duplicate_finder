from typing import Union, List, Dict
import os

from fastapi import FastAPI
from src.duplicate_finder import find_duplicates
from src.vector_data_manager import write_documents
from src.vector_data_manager import load_document_store
import json


app = FastAPI()



document_store_dir = ".data/document_store/"
index_name_global = "new_faiss_index.faiss"
document_store = load_document_store(document_store_dir, index_name_global)

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



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/duplicates")
def get_duplicates(text_list:List[dict], retriever_k=10, ranker_k=5):
    text_batch = []
    for text_dict in text_list:
        text = text_dict["title"]+"\n"+text_dict["content"]
        text_batch.append(text)
    return find_duplicates(text_batch[0], retriever_k, ranker_k)

@app.post("/duplicates_batch")
def get_duplicates_batch(text_list:List[dict], retriever_k=10, ranker_k=5):
    text_batch = []
    for text_dict in text_list:
        text = text_dict["title"]+"\n"+text_dict["content"]
        text_batch.append(text)
    return find_duplicates_batch(text_batch, retriever_k, ranker_k)

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

    
# if __name__ == "__main__":
#     from src.vector_data_manager import prepare_documents, write_documents

#     #create the document store
#     data_path = ".data/AI Sample Data.xlsx"
#     documents = prepare_documents(data_path)
#     document_store_dir = ".data/document_store/"
#     index_name = "new_faiss_index.faiss"
#     index_path = document_store_dir+index_name
#     #write documents to the document store
#     write_documents(documents, document_store, retriever)
#     document_store.save(index_path=index_path)
    
    # Saving the document store creates two files: my_faiss_index.faiss and my_faiss_index.json
    # index_path = write_documents(documents, document_store,retriever)