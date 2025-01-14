from pymongo.mongo_client import MongoClient

url = 'mongodb+srv://danil:mypassword@cluster0.dycl0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(url)

db = client.kitchen
recipe_collections = db['kitchenList']

try:
    client.admin.command("ping")
    print("Connected to MongoDB successfully")
except Exception as e:
    print(e)

