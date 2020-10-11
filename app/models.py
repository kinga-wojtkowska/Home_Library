from app import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)

    def __repr__(self):
        return f"{self.name}"


book_author = db.Table('join',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    year = db.Column(db.Numeric(4, 0))
    author = db.relationship('Author', secondary=book_author, backref=db.backref('books', lazy='dynamic'))  # noqa: E501
    borrowed = db.relationship('Borrowing', backref='book')

    def __repr__(self):
        if self.borrowed:
            return f"{self.title}, {self.author}, {self.year}, {self.borrowed[-1]}"  # noqa: E501
        else:
            return f"{self.title}, {self.author}, {self.year}, the book is at home!"  # noqa: E501


class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrowed = db.Column(db.Boolean())
    borrow_date = db.Column(db.String(10))
    where = db.Column(db.String(50))
    id_book = db.Column(db.String, db.ForeignKey('book.title'))

    def __repr__(self):
        if self.borrowed is True:
            return f"borrowed to {self.where}, {self.borrow_date}"
        else:
            return f"the book is at home!"
