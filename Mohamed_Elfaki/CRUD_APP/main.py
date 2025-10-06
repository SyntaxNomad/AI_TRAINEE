from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session
import database
from typing import Optional
from fastapi import Query

app = FastAPI()


sqlite_url = "sqlite:///database.db" 
engine = create_engine(sqlite_url, echo=True)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/items/")
def add( title, author, category, status):
    bid = database.add_db(title=title,author=author,category=category,status=status)
    return{
        "message":"Book added successfully",
        "book": {
            "bid": bid,
            "title": title,
            "author": author,
            "category": category,
            "status": status
        }
    }


@app.delete("/items/{bid}")
def delete(bid):
    message = database.delete_book_by_bid(bid=bid)
    return{
        "message":message
    }
    


@app.put("/items/{bid}")
def update(
    bid: int,
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    success, returned_bid, returned_title, returned_author, returned_category, returned_status = database.update_db(
        bid=bid,
        title=title,
        author=author,
        category=category,
        status=status
    )
    
    # Check if update was successful
    if "does not exist" in success:
        return {
            "error": success,
            "bid": bid
        }
    
    return {
        "message": success,
        "book": {
            "bid": returned_bid,
            "title": returned_title,
            "author": returned_author,
            "category": returned_category,
            "status": returned_status
        }
    }

@app.get("/items/all")
def read_all():
    data = database.read_all()
    return data

@app.get("/items/{bid}")
def read(bid: int):
    ok, data = database.read(bid)
    return {
        "success": ok,
        "book": data
    }

@app.post("/item-borrow")
def borrow(bid: int):
    ok = database.borrow(bid)
    return {"message":ok}

@app.post("/item-return")
def return_book(bid: int):
    ok = database.return_book(bid)
    return {"message": ok }