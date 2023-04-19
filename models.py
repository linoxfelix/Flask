from flsk_app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Role('{self.name}')"



class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(200), nullable=False)
    gr_level = db.Column(db.String(50), nullable=False)
    num_copies = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric, nullable=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.gr_level}', '{self.num_copies}')"

    def borrow(self, student):
        if self.num_copies > 0:
            loan = Loan(book_id=self.id, student_id=student.id)
            self.num_copies -= 1
            db.session.add(loan)
            db.session.commit()
            return True
        else:
            return False

    def reserve(self, student):
        if self.num_copies == 0:
            reservation = Reservation(book_id=self.id, student_id=student.id)
            db.session.add(reservation)
            db.session.commit()
            return True
        else:
            return False
class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    reserved_date = db.Column(db.Date)

    def __repr__(self):
        return f"<Reservation {self.student_id} {self.book_id} {self.reserved_date}>"

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    def __repr__(self):
        return f"<Loan {self.student_id} {self.book_id} >"

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Author('{self.first_name}', '{self.last_name}')"


class Student(User):
    def borrow_book(self, book_id):
        book = Book.query.get(book_id)
        if book and self.gr_level >= book.gr_level:
            return book.borrow(self)
        else:
            return False

    def reserve_book(self, book_id):
        book = Book.query.get(book_id)
        if book and self.gr_level >= book.gr_level:
            return book.reserve(self)
        else:
            return False


class Teacher(User):
    def update_gr_level(self, student_id, gr_level):
        student = Student.query.get(student_id)
        if student:
            student.gr_level = gr_level
            db.session.commit()

    def update_student_info(self, student_id, username, email):
        student = Student.query.get(student_id)
        if student:
            student.username = username
            student.email = email
            db.session.commit()


class Parent(User):
    def buy_book(self, book_id):
        book = Book.query.get(book_id)
        if book and book.num_copies == 0:
            book.num_copies = 1
            db.session.commit()
            return True
        else:
            return False
