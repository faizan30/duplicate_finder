
def find_duplicates(text, retriever_k=10, ranker_k=5):
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
    