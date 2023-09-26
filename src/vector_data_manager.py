import os
from typing import List
from haystack.document_stores import FAISSDocumentStore

def load_document_store(document_store_dir=".data/document_store/", index_name="new_faiss_index.faiss"):
    """Load the document store"""
    # load the document store:
    index_path = document_store_dir+index_name
    if not os.path.exists(document_store_dir):
        os.makedirs(document_store_dir)
    if not os.path.exists(index_path):
        document_store = FAISSDocumentStore(vector_dim=128, faiss_index_factory_str="Flat")
    else:
        document_store = FAISSDocumentStore.load(index_path=index_path)
    return document_store


def write_documents(documents: List[dict], document_store, retriever=None):
    """Write documents to the document store"""
    document_store.write_documents(documents)
    document_store.update_embeddings(retriever)
    


def prepare_documents(data_path):
    """Prepare documents in the form of dictionaries"""
    import uuid
    import pandas as pd
    df = pd.read_excel(data_path)
    df["content"] = df["Idea Title"]+"\n"+df["Idea Description"]
    df["Idea ID"] = df.apply(lambda x: str(uuid.uuid4()), axis=1)
    df["meta"] = df.apply(lambda x: {"name":x["Idea Title"], "id":x["Idea ID"]}, axis=1)
    documents = df.to_records()
    
    docs = []
    for i in  range(len(documents)):
        doc ={}
        doc['content'] = documents[i]['content']
        doc['meta'] = documents[i]['meta']
        docs.append(doc)

    return docs


    
    


