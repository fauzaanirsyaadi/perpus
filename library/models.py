from app import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    __tablename__ = 'user'

    studentId = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(28), nullable=False, unique=True)
    public_id = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    password= db.Column(db.String(120), nullable=False)
    borrow=db.relationship('borrow', backref='borrower', lazy='dynamic')

    def set_password(self, password):
      self.password = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password, password)

    @staticmethod
    def get_user(id):
      return User.query.get(int(id))
    
    def get_json(self):
      return{
        'id': self.public_id, 'name': self.name, 
        'email': self.email, 'is admin': self.is_admin,
        'borrow': self.borrow.all()
      }
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
      return f'User <{self.email}>'

class Borrow(db.Model):
    __tablename__ = 'borrow'

    borrowId = db.Column(db.Integer, primary_key=True, index=True)
    studentId = db.Column(db.String(80), nullable=False)######
    bookId=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#####
    takenDate= db.Column(db.String, nullable=False)########
    broughtDate= db.Column(db.String, nullable=False)######
    
    def get_json(self):
      return { 
        'id': self.public_id, 'name': self.name,
        'completed': self.is_completed,
        'borrower': {
          'name': self.borrower.name,
          'email': self.borrower.email,
          'public_id': self.borrower.public_id
        }
      }
    
    def __repr__(self):
      return f'borrow: <{self.name}>'


class Book(db.Model):
    __tablename__ = 'book'

    bookId = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    pagecount = db.Integer(db.String(50))#######
    point=db.Column(db.String(50))######
    author = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))
    borrow_book = db.relationship('Borrow', backref='book', lazy='dynamic')####

    def __repr__(self):
        return f'Book <{self.book_title}>'