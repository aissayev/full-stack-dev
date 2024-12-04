from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Create a MongoDB client
client = AsyncIOMotorClient("mongodb://localhost:27017")

# Access a database and collection
db = client.fullstack
collection = db.students

# async def insert_one_document():
#     document = {"name": "Adilet", "age": 30, "email": "adilet@example.com"}
#     result = await collection.insert_one(document)
#     print(f"Inserted document ID: {result.inserted_id}")

# # Example usage in an async context

# asyncio.run(insert_one_document())


async def find_all_documents():
    async for doc in collection.find():
        print(doc)

# Example usage in an async context
asyncio.run(find_all_documents())