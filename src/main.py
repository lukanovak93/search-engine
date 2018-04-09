from pymongo import MongoClient

if __name__ == '__main__':

    client = MongoClient()
    db = client.Database
    vocab = db.Vocab
    documents = db.Documents

    
