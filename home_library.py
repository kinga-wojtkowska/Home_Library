from app import app, db
from app.models import Author, Borrowing, Book


@app.shell_context_processor
def make_shell_context():
    return {
       "db": db,
       "Book": Book,
       "Author": Author,
       "Borrowing": Borrowing
    }
