from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import base64

# initializing our app
app = Flask(__name__)
migrate = Migrate(app, db)
# app.debug = True

# Configs
# Replace the user, password, hostname and database according to your configuration information
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost:5432/library'

# Modules
db = SQLAlchemy(app)

class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    books = db.relationship('Book', backref='author')
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'User <{self.id}>'

class Book(db.Model):
    __tablename__ = 'books'
    
    book_code = db.Column(db.Integer, primary_key=True, index=True)
    book_title = db.Column(db.String, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50))
    genres = db.Column(db.String(50))
    stock = db.Column(db.Integer, nullable=False)
    borrow_book = db.relationship('Borrowing', backref='borbo', lazy='dynamic')

    def __repr__(self):
        return f'Book <{self.book_title}>'

class Borrowing(db.Model):
    borrowing_id = db.Column(db.Integer, primary_key=True, index=True)
    book_code = db.Column(db.Integer, db.ForeignKey('book.book_code'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    borrow_from_date = db.Column(db.String(25), nullable=False)
    borrow_to_date = db.Column(db.String(25), nullable=False)
    book_status = db.Column(db.Boolean, default=False)

@app.route('/users/')
def get_users():
    return jsonify([
        {
            'user_id': user.user_id, 'user_name': user.user_name, 'email': user.email
        } for user in User.query.all()
    ])

@app.route('/users/<id>/')
def get_user(id):
    print(id)
    user = User.query.filter_by(user_id=id).first_or_404()
    return {
        'user_id': user.user_id, 'user_name': user.user_name, 'email': user.email
    }

@app.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not 'user_name' in data or not 'email' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name or email not given'
        }), 400
    u = User(
            email=data['email'],
            user_name=data['user_name'],
            password=data['password']
        )
    db.session.add(u)
    db.session.commit()
    return {
        'user_id': u.user_id, 'user_name': u.user_name, 'email': u.email
    }, 201

@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    if not 'user_name' in data and not 'email' in data and not 'password' in data:
        return {
            'error': 'Bad Request',
            'message': 'field needs to be present'
        }, 400
    user = User.query.filter_by(user_id=id).first_or_404()
    if 'user_name' in data:
        user.user_name = data['user_name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    db.session.commit()
    return jsonify({
        'success': 'data has been changed successfully',
        'user_id': user.user_id, 'user_name': user.user_name, 'email': user.email
    })

@app.route('/users/<id>/', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(user_id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }


@app.route('/books/')
def get_books():
    return jsonify([
        {
            'book_code': book.book_code, 'book_title': book.book_title, 'author': book.author,
            'publisher': book.publisher, 'genres': book.genres, 'stock': book.stock
        } for book in Book.query.all()
    ])

@app.route('/books/<id>/')
def get_book(id):
    book = Book.query.filter_by(book_code=id).first_or_404()
    return {
        'book_code': book.book_code, 'book_title': book.book_title, 'author': book.author,
        'publisher': book.publisher, 'genres': book.genres, 'stock': book.stock
    }

@app.route('/books/', methods=['POST'])
def add_book():
    data = request.get_json()
    if not 'book_title' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Book Title not given'
        }), 400
    book = Book(
            book_title = data['book_title'],
            author = data['author'],
            publisher = data['publisher'],
            genres = data['genres'],
            stock = data['stock']
        )
    db.session.add(book)
    db.session.commit()
    return {
        'book_code': book.book_code, 'book_title': book.book_title, 'author': book.author,
        'publisher': book.publisher, 'genres': book.genres, 'stock': book.stock
    }, 201


@app.route('/books/<id>/', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(book_code=id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }


@app.route('/borrow/')
def get_borrow():
    return jsonify([
        {
            'book': {
                'book code': borrowing.borbo.book_code,
                'book title': borrowing.borbo.book_title,
                'author': borrowing.borbo.author,
                'publisher': borrowing.borbo.publisher
            },
            'borrowing id': borrowing.borrowing_id, 'start date': borrowing.borrow_from_date,
            'end date': borrowing. borrow_to_date,
            'borrower': {
                'user id': borrowing.borus.user_id,
                'name': borrowing.borus.user_name,
                'email': borrowing.borus.email
            }
        } for borrowing in Borrowing.query.all()
    ])

@app.route('/borrow/', methods=['POST'])
def add_borrow():
    data = request.get_json()
    header = request.headers.get('authorization')
    plain = base64.b64decode(header[6:]).decode('utf-8')
    planb = plain.split(":")
    user = User.query.filter_by(user_name=planb[0], password=planb[1]).first_or_404()
    book = Book.query.filter_by(book_title=data['book_title']).first_or_404()
    if planb[0] in user.user_name and planb[1] in user.password:
        if (not 'borrow_from_date' in data) or (not 'borrow_to_date' in data):
            return jsonify({
                'error': 'Bad Request',
                'message': 'user id or book code not given'
            }),400
        borrow = Borrowing(
                book_code = book.book_code,
                user_id = user.user_id,
                borrow_from_date = data['borrow_from_date'],
                borrow_to_date = data['borrow_to_date']
            )
        db.session.add(borrow)
        db.session.commit
        return {
            'book': {
                'book code': borrow.book_code,
                'book title': book.book_title,
                'author': book.author,
                'publisher': book.publisher
            },
            'borrowing id': borrow.borrowing_id, 'start date': borrow.borrow_from_date,
            'end date': borrow. borrow_to_date,
            'borrower': {
                'user id': borrow.user_id,
                'name': user.user_name,
                'email': user.email
            }
        }, 201


@app.route("/")
@app.route("/home")
def home():
    return {
        'greeting':'halo dunia, selamat datang di library'
    },200

if __name__ == '__main__':
    app.run(debug=True)