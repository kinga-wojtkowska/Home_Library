from app import db

book_author = db.Table('join',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    year = db.Column(db.Numeric(4, 0))
    author = db.relationship('Author', secondary=book_author, backref=db.backref('books', lazy='dynamic'))
    borrowed = db.relationship('Borrowing', backref='book')

    def __repr__(self):
        if self.borrowed:
            return f"Book: {self.title}, {self.author}, {self.year}, {self.borrowed[-1]}"
        else:
            return f"Book: {self.title}, {self.author}, {self.year}, the book is at home!"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)

    def __repr__(self):
        return f"Author: {self.name}"


class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrowed = db.Column(db.Boolean())
    borrow_date = db.Column(db.String(10))
    where = db.Column(db.String(50))
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __repr__(self):
        if self.borrowed == True:
            return f"borrowed to {self.where}, {self.borrow_date}"
        else:
            return f"the book is at home!"
