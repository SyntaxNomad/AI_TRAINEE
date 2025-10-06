from sqlmodel import Field, SQLModel, create_engine, Session
from sqlalchemy import select
from fastapi import Query

# DB = "database.db"
# CSV = "data.csv" 

# con = sqlite3.connect(DB)
# cur = con.cursor()
# cur.execute("""
# CREATE TABLE IF NOT EXISTS books (
#   bid INTEGER PRIMARY KEY,
#   title TEXT,
#   author TEXT,
#   category TEXT,
#   status TEXT
# );
# """)

# with open(CSV,newline="", encoding="utf-8") as fin:

#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['bid'], i['title'],i['author'],i['category'],i['status']) for i in dr]

# cur.executemany("INSERT INTO books (bid, title, author, category, status) VALUES (?, ?, ?, ?, ?);", to_db)
# con.commit()
# con.close() 
class books(SQLModel,table=True):
    bid: int | None = Field(default=None, primary_key=True, nullable=False)
    title: str
    author: str
    category: str
    status: str


engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)

def add_db(title, author, category, status):
    with Session(engine) as session:
        newbook = books(title=title, author=author, category=category, status=status)
        session.add(newbook)
        session.commit()
        session.refresh(newbook)
        bid = newbook.bid
        return bid
        


def update_db(bid, title=None, author=None, category=None, status=None):
    with Session(engine) as session:
        book = session.get(books, bid)
        if book:
            if title is not None:
                book.title = title
            if author is not None:
                book.author = author
            if category is not None:
                book.category = category
            if status is not None:
                book.status = status
            session.commit()
            # Return 5 values, not 6
            return "Successful Update", book.bid, book.title, book.author, book.category, book.status
        else:
            # Return 5 values for error case too
            return f"Book with bid={bid} does not exist", bid, None, None, None, None


def delete_book_by_bid(bid):
    with Session(engine) as session:
        book = session.get(books, bid)
        if book:
            session.delete(book)
            session.commit()
            return f"Deleted book with bid={bid}"
        else:
            return f"No book found with bid={bid}"




def read(bid: int):
    with Session(engine) as session:
        book = session.get(books, bid)
        if not book:
            return False, None
        return True, {
            "bid": book.bid,
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "status": book.status
        }
    
def read_all():
    with Session(engine) as session:
        statement = select(books)
        books_list = session.scalars(statement).all()
        return [
            {
                "bid": book.bid,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "status": book.status
            }
            for book in books_list
        ]

            

def borrow(bid):
    with Session(engine) as session:
        book = session.get(books,bid)
        try:
            if book.status.lower() =="issued":
                return "Book has already been borrowed"
            elif book.status.lower() =="available":
                book.status = "issued"
                session.commit()
                return f"You have Successfully borrowed the book bid: {bid} , name {book.title}"
        except:
            return f"This Book doesnt bid:{bid} exist"
        

def return_book(bid):
    with Session(engine) as session:
        book = session.get(books,bid)
        try:
            if book.status.lower() =="issued":
                book.status="available"
                session.commit()
                return f"You have successfully returned the book bid: {bid} , name {book.title}"
            
            elif book.status.lower() == "available":
                return "This book hasn't been borrowed"
        except:
            return f"This Book doesnt bid:{bid} exist"