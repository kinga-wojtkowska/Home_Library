from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired
from app.models import Book, Author

authors = Author.query.all()
books_all = Book.query.all()
books = [x.title for x in books_all]


class BooksLibForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    year = IntegerField('Rok wydania')
    author = SelectField('Wybierz autora', choices=authors)


class AuthorLibForm(FlaskForm):
    name = StringField('Autor', validators=[DataRequired()])


class BorrowingForm(FlaskForm):
    title = SelectField('Wybierz tytuł książki', choices=books)
    date = StringField('Data wypożyczenia, YYYY-MM-DD', validators=[DataRequired()])
    where = StringField('Komu wypożyczono', validators=[DataRequired()])


class DeleteForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
