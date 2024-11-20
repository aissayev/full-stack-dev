from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI behind Nginx - This is Lesson 8 - Have Fun"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/lesson-8")
def read_item(item_id: int, q: str = None):
    return {"Congrats you completed Lesson 8 and now you know hot setup server and api"}