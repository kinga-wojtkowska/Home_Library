from flask import Flask, jsonify, abort, make_response, request, render_template  # noqa: E501
from app import db, app
from app.models import Book, Author, Borrowing
from app.forms import BooksLibForm, AuthorLibForm, DeleteForm, BorrowingForm


# wyświetla wszystkie książki w bazie lub tworzy nową pozycję książkową
@app.route("/sql/books/", methods=["GET", "POST"])
def books_list_sql():
    form = BooksLibForm()
    books_all = Book.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            book1 = Book(title=form.title.data, year=form.year.data)
            db.session.add(book1)
            db.session.commit()
            author1 = Author.query.filter_by(name=form.author.data).first()
            author1.books.append(book1)
            db.session.commit()
            books_all = Book.query.all()
            return render_template("books.html", books=books_all, form=form)
    return render_template("books.html", books=books_all, form=form)


# wyświetla wszystkich autorów w bazie lub tworzy nową pozycję autora
@app.route("/sql/authors/", methods=["GET", "POST"])
def authors_list_sql():
    form = AuthorLibForm()
    authors = Author.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            author1 = Author(name=form.name.data)
            db.session.add(author1)
            db.session.commit()
            authors = Author.query.all()
            return render_template("authors.html", authors=authors, form=form)
    return render_template("authors.html", authors=authors, form=form)


@app.route("/sql/borrowing/", methods=["GET", "POST"])
def borrowing_list_sql():
    form = BorrowingForm()
    form2 = DeleteForm()
    borrowing = Borrowing.query.all()
    books = Book.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            book1 = Book.query.filter_by(title=form.title.data).first()
            borrow = Borrowing(borrowed=True, borrow_date=form.date.data, where=form.where.data, book=book1)  # noqa: E501
            db.session.add(borrow)
            db.session.commit()
            borrowing = Borrowing.query.all()
            return render_template("borrowing.html", borrowing=borrowing, form=form, form2=form2)  # noqa: E501
        if form2.validate_on_submit():
            borrow = Borrowing.query.filter_by(id=form2.id.data).first()
            borrow.borrowed = False
            db.session.commit()
            return render_template("borrowing.html", borrowing=borrowing, form=form, form2=form2)  # noqa: E501
    return render_template("borrowing.html", borrowing=borrowing, form=form, books=books, form2=form2)  # noqa: E501


# pokazuje konkretny rekord z bazy danych, pozwala na zmianę danych lub usunięcie książki  # noqa: E501
@app.route("/sql/books/<int:book_id>", methods=["GET", "POST"])
def get_book(book_id):
    form = BooksLibForm()
    book = Book.query.get(book_id)
    if request.method == "POST":
        book = Book.query.get(book_id)
        book.title = form.title.data
        book.year = form.year.data
        db.session.commit()
        author1 = Author.query.filter_by(name=form.author.data).first()
        author1.books.append(book)
        db.session.commit()
        return render_template("book.html", book=book, form=form, book_id=book_id)  # noqa: E501
    return render_template("book.html", book=book, form=form, book_id=book_id)


@app.route("/sql/authors/<int:author_id>", methods=["GET", "POST"])
def get_authors_books(author_id):
    form = DeleteForm()
    author = Author.query.get(author_id)
    books = author.books
    if not author:
        abort(404)
    if request.method == "POST":
        book = Book.query.filter_by(id=form.id.data).first()
        author.books.remove(book)
        db.session.commit()
        return render_template("author_books.html", author=author.name, books=books, author_id=author_id, form=form)  # noqa: E501
    return render_template("author_books.html", author=author.name, books=books, author_id=author_id, form=form)  # noqa: E501


# usuwa rekord książki o danym id z bazy danych
@app.route("/sql/books/delete/<int:book_id>", methods=['GET'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return render_template("books.html", books=Book.query.all(), form=BooksLibForm())  # noqa: E501


# usuwa rekord autora z bazy danych
@app.route("/sql/authors/delete/<int:author_id>", methods=['GET'])
def delete_author(author_id):
    author = Author.query.get(author_id)
    db.session.delete(author)
    db.session.commit()
    return render_template("authors.html", authors=Author.query.all(), form=AuthorLibForm())  # noqa: E501


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)  # noqa: E501


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)  # noqa: E501
