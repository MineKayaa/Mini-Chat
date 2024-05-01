import pymongo
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

CONN_STRING = os.getenv('CONN_STRING')

client = MongoClient(CONN_STRING)

class dal:
    def db_health_check():
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)   
    def init_collection():
        db = client.mini_chat_db
        my_collection = db["chat_history"]
        chats = [{ "chat_id": "1", "messages": ["hi", "hi, how are you"] },
                    { "chat_id": "2", "messages": ["hello", "how you doing"] }]
        try: 
            result = my_collection.insert_many(chats)
            # return a friendly error if the operation fails
        except pymongo.errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        else:
            inserted_count = len(result.inserted_ids)
            print("I inserted %x documents." %(inserted_count))
            print("\n")
    def get_collection():
        db = client.mini_chat_db
        my_collection = db["chat_history"]
        return my_collection
    
    def get_messages(chat_id: str):
        my_collection = dal.get_collection()
        result = my_collection.find({"chat_id": chat_id})
        messages = ""
        if result:    
            for doc in result:
                chat_id = doc['chat_id']
                messages_count = len(doc['messages'])
                messages += ' '.join(doc['messages'])
                messages += "\n"
            return messages
        else:
            print("No documents found.")
            return ""
        
    def insert_message(chat_id: str, ai_message : str, human_message : str):
        my_collection = dal.get_collection()
        chat = [{ "chat_id": chat_id, "messages": [human_message , ai_message] }]
        try: 
            result = my_collection.insert(chat)
        except pymongo.errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        else:
            print("I inserted document.")
            print("\n")
    
    def get_last_chat_id():
        my_collection = dal.get_collection()
        result = my_collection.find()
        chat_array = []
        if result:    
            for doc in result:
                chat_id = doc['chat_id']
                chat_array.append(int(chat_id))
            return max(chat_array)
        else:
            print("No documents found.")
            return 0
        