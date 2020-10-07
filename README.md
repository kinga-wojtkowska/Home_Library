#Home_Library
1. Welcome to my home_library app!
2. Initially, you can test the application with the test database that is attached.
3. If you want to create your own home library, delete the database and the 'migrations' folder, and then after starting the virtual environment, enter a few commands in the command line:
- flask db init
- flask db migrate -m "create tables and relations"
- flask db upgrade
4. This will create an empty database with the necessary tables.
5. The requirements.txt file contains all the modules that are needed for the application to work properly.
6. After typing 'flask shell' inside your installed venv, you can perform various operations on the database.
7. With the help of appropriate queries, you can add to the database: authors, books and information whether the book has been lent to someone.
8. Adding author (class Author):
    - author1 = Author(name="type_author_fullname")
    - db.session.add(author1)
    - db.session.commit()
9. Remember to always commit changes if you want to see them in your database.
10. Adding book (class Book) is the same but with different parameters: title="type_title", year=YYYY
11. If you want to connect book with author you need to type: author1.books.append(book1) and then commit changes.
12. Adding borrowing (class Borrowing) record is the same but with different parameters:
    - you need to define which book you want to lend - book1 = Book.query.get(1)
    - borrowed (True or False), borrow_date = "YYYY-MM-DD", where="type_where", book=book1
    - then you can type book1 and you will see information about it
13. Before adding a new record, you can check whether, for example, a given author is already in the database:
    - authors = Author.query.all()
    - for i in authors: print(i)
14. If you want to see all books assigned to a given author type as below:
    - author3 = Author.query.get(3)
    - pratchett = author3.books
    - for i in pratchett: print(i)