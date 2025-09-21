from typing import Union

from fastapi import FastAPI

app = FastAPI()



@app.get("/bookname")
def getBook():
    bookname="ramayan"
    return bookname



@app.get("/")
def read_root():
    return {"Hello": "API"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None,cos:Union[str, None] = None):
    return {"item_id": item_id, "q": q}
