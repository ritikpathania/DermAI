from pymongo import MongoClient

client = MongoClient("mongodb+srv://ritikpathania:btd3xkx.UWG-qxf-paz@cluster0.fmmyiii.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.todo_db

collection_name = db["todo_collection"]