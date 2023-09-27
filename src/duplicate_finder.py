# RANKER INITIALIZATION
from haystack.nodes import BM25Retriever, SentenceTransformersRanker
from haystack.nodes import EmbeddingRetriever

ranker_model = "cross-encoder/ms-marco-MiniLM-L-12-v2"
ranker = SentenceTransformersRanker(model_name_or_path=ranker_model)

def set_retriever(document_store, embedding_model = "yjernite/retribert-base-uncased", model_format = "retribert"):
    # RETRIEVER INITIALIZATION
    retriever = EmbeddingRetriever(document_store=document_store,
                                embedding_model=embedding_model,
                                model_format=model_format)

    return retriever



def find_duplicates(text, retriever, ranker, retriever_k=10, ranker_k=5):
    '''Given a text paragraph, find if the duplicates exist in a vector database'''
    
    candidate_duplicates = retriever.retrieve(query=text, top_k=retriever_k)
    
    duplicates = ranker.predict(query=text, documents=candidate_duplicates, top_k=ranker_k)
    
    print(duplicates)
    return duplicates

def find_duplicates_batch(text_list, retriever_k=10, ranker_k=5):
    '''Given a text paragraph, find if the duplicates exist in a vector database'''
    
    candidate_duplicates = retriever.retrieve(query=text, top_k=retriever_k)
    
    duplicates = ranker.run_batch(query=text, documents=candidate_duplicates, top_k=ranker_k)
    
    print(duplicates)
    return duplicates
    