


def find_duplicate(text, threshold=0.7):
    '''Given a text paragraph, find if the duplicates exist in a vector database'''
    
    duplicates = {"duplicates":[
        {
            "id": 1,
            "text": "This is a duplicate text",
            "similarity": 0.9
        },
        {
            "id": 2,
            "text": "This is another duplicate text",
            "similarity": 0.8
        }
        ]
        }
    return duplicates