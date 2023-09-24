import os
from typing import List
from haystack.document_stores import FAISSDocumentStore

document_store_dir = ".data/document_store/"
index_path = document_store_dir+"my_faiss_index.faiss"

if not os.path.exists(document_store_dir):
    os.makedirs(document_store_dir)

def create_document_store(index_path, faiss_index_factory_str="Flat"):
    '''Create the document store'''
    document_store = FAISSDocumentStore()
    document_store.save(index_path=index_path)
    return document_store


def load_document_store(index_path):
    """Load the document store"""
    # load the document store:
    document_store = FAISSDocumentStore.load(index_path=index_path)
    return document_store

# dicts = [
#     {
#         'content': DOCUMENT_TEXT_HERE,
#         'meta': {'name': DOCUMENT_NAME, ...}
#     }, ...
# ]

def write_documents(documents: List[dict], document_store, retriever=None):
    """Write documents to the document store"""
    document_store.write_documents(documents)
    # Saving the document store creates two files: my_faiss_index.faiss and my_faiss_index.json
    document_store.save(index_path=index_path)
    # when using a dense retriever like embedding retriever, or Dense Passage Retrieval
    if retriever:
        document_store.update_embeddings(retriever)
    return document_store


def document_store_stats(document_store):
    """Get document store meta and return"""
    return {}


def prepare_documents(data_path):
    """Prepare documents in the form of dictionaries"""
    documents = []

    return documents

if __name__ == "__main__":
    data_path = ""

    # create the document store
    document_store = create_document_store(index_path)
    # documents = prepare_documents(data_path)
    # write documents to the document store
    # write_documents(documents, document_store)
    
    # document_store = load_document_store(index_path)
    # write_documents(documents, document_store)
    data_path = ".data/AI Sample Data.xlsx"
    import pandas as pd
    df = pd.read_excel(data_path)
    # dicts = [
    #     {
    #         'content': DOCUMENT_TEXT_HERE,
    #         'meta': {'name': DOCUMENT_NAME, ...}
    #     }, ...
    # ]
    df.renamee(columns={"Idea Description":"content"}, inplace=True)
    df["meta"] = df.apply(lambda x: {"name":x["Idea Title"], "id":x["Idea ID"]}, axis=1)
    documents = df.to_records()


