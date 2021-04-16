import os, uuid, jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import base64
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
# bcrypt = Bcrypt(app)
db = SQLAlchemy()

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@localhost:5432/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

class Users(db.Model):
    userId = db.Column(db.Integer, primary_key=True, index=True)
    userName = db.Column(db.String(30), nullable=False)
    password= db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    address = db.Column(db.String(50), nullable=False)
    public_id = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    borrow=db.relationship('Borrow', backref='borrower', lazy='dynamic')

    def __repr__(self):
        return f'Users<{self.email}>'

class Borrow(db.Model):
    borrowId = db.Column(db.Integer, primary_key=True, index=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    bookId=db.Column(db.Integer, db.ForeignKey('book.bookId'), nullable=False)
    takenDate= db.Column(db.String(30), nullable=False)
    broughtDate= db.Column(db.String(30), nullable=False)
    returnDate = db.Column(db.String(25), nullable=False)
    borrowStatus = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Borrow<{self.borrowId}>'
    
class Book(db.Model):
    bookId = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50))
    copies = db.Column(db.String(3), nullable=False)
    borrow_book = db.relationship('Borrow', backref='book', lazy='dynamic')####
    
    def __repr__(self):
        return f'Book<{self.title}>'

@app.route('/users/')
def get_users():

    return jsonify([
        {
            'userId': user.userId, 
			'name': user.userName, 
			'email': user.email,
			'phone': user.phone,
			'address': user.address
            } for user in Users.query.all()
    ])
	
@app.route('/login_users/', methods = ['POST'])
def login_users():
    data = request.get_json()
    if not 'email' in data and not 'password' in data:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Email or password must be given'
        }), 400
    
    try:
        user = Users.query.filter_by(email = data["email"]).first_or_404()
    except:
        return jsonify ({
            "message" : "Invalid email or password!"
        }), 401

    payload = {'userID': user.userID, 'email': user.email}

    encoded_jwt = jwt.encode(payload, "secret", algorithm="HS256")

    if bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify ({
            'userID': user.userID, 
            'name': user.name, 
            'email': user.email, 
            'password' : user.password,
            'access_token': encoded_jwt.decode('utf-8')
        })
    else:
        return jsonify ({
            "message" : "Invalid email or password!"
        }), 401

@app.route('/users/<id>/')
def get_user(id):
    print(id)
    user = Users.query.filter_by(userId=id).first_or_404()
    return {
        'userId': user.userId,
		'name': user.userName, 
		'email': user.email,
		'password': user.password,
		'address':user.address,
		'phone':user.phone
    }

@app.route('/users/', methods=['POST'])
def create_user():
	data = request.get_json()
	if not 'userName' in data or not 'email' in data or 'password' in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name, email or password not given'
		}), 400
	if len(data['userName']) < 4 or len(data['email']) < 6:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name and email must be contain minimum of 4 letters'
		}), 400
	u = Users(
			userName=data['userName'], 
			email=data['email'],
            password=data['password'],
			phone=data['phone'],
			address=data['address'],
			is_admin=data.get('is admin', False),
			public_id=str(uuid.uuid4())
		)
	db.session.add(u)
	db.session.commit()
	return {
        'userId': u.userId, 'userName': u.userName, 'email': u.email
    }, 201
    
@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    if not 'userName' in data and not 'email' in data and not 'password' in data:
        return {
            'error': 'Bad Request',
            'message': 'field needs to be present'
        }, 400
    user = Users.query.filter_by(userId=id).first_or_404()
    if 'userName' in data:
        user.userName = data['userName']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
	# if 'phone' in data:
    # 	user.phone = data['phone']
	# if 'address' in data:
    #     user.address = data['address']
    db.session.commit()
    return jsonify({
        'success': 'data has been updated successfully',
        'userId': user.userId, 
		'name': user.name, 
		'email': user.email,
		'phone': user.phone,
		'address': user.address
    })

@app.route('/users/<id>/', methods=['DELETE'])
def delete_user(id):
    user = Users.query.filter_by(userId=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }

##########################################################

@app.route('/borrow/')
def get_borrow():
    header = request.headers.get('authorization')#basic out postman
    plain = base64.b64decode(header[6:]).decode('utf-8')#ada basic(ingin dibuang)
    planb = plain.split(":")# , username password,
    user = Users.query.filter_by(name=planb[0], password=planb[1]).first_or_404()# ngecheck planb, manggil class user,
    if planb[0] in user.name and planb[1] in user.password:
        return jsonify([ #untuk bisa looping langsung
            {
                'book': {
                    'book code': borrow.books.bookID,# looping
                    'book title': borrow.book.title,
                    'author': borrow.book.author,
                    'publisher': borrow.book.publisher
                },
                'Borrow id': borrow.borrowId, # 
				'start date': borrow.takenDate,
                'end date': borrow.broughtDate, #
                'borrower': {
                    'user id': borrow.borrower.userId,
                    'name': borrow.borrower.userName,
                    'email': borrow.borrower.email,
					'phone': borrow.borrower.phone
                }
            } for borrow in Borrow.query.all() #ambil borrow sebagai perulangan 
        ])


@app.route('/borrow/', methods=['POST'])
def add_borrow():
    data = request.get_json()
    header = request.headers.get('authorization')
    plain = base64.b64decode(header[6:]).decode('utf-8')
    planb = plain.split(":")
    user = Users.query.filter_by(userName=planb[0], password=planb[1]).first_or_404()
    book = Book.query.filter_by(bookID=data['bookID']).first() # select * from book where bookID = data inputan, query filter
    count = Borrow.query.filter_by(borrowStatus=False, bookID=data['bookID']).count() # select count(*) from book where borrow status = false and bookID =datainputan 
    if planb[0] in user.userName and planb[1] in user.password: #
        if not 'userId' in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'user id of borrower not given'
            }),400
        if not 'bookID' in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'book code to borrow not given'
            }),400
        if (not 'takenDate' in data) or (not 'broughtDate' in data):
            return jsonify({
                'error': 'Bad Request',
                'message': 'borrow start date and end date not given'
            }),400
        if count == book.copies:
            return jsonify({
                'Sorry': 'book is not available'
            }),400
        else:
            borrow = Borrow(
                    bookId = data['bookId'],
                    userId = data['userId'],
                    takenDate = data['takenDate'],
                    broughtDate = data['broughtDate'],
                    borrowStatus = data['borrowStatus']
                )
            db.session.add(borrow)
            db.session.commit()
            return {
                'borrowId': borrow.borrowId, 
				'start date': borrow.takenDate,
                'end date': borrow.broughtDate,
                'book': {
                    'book code': borrow.book.bookID,
                    'book title': borrow.book.title,
                    'author': borrow.book.author,
                    'publisher': borrow.book.publisher
                },
                'borrower': {
                    'user id': borrow.borrower.userId,
                    'name': borrow.borrower.userName,
                    'email': borrow.borrower.email
                }
            }, 201


app.route('/borrow/<id>/', methods=['PUT'])
def return_borrow(id):
    data = request.get_json()
    header = request.headers.get('authorization')
    plain = base64.b64decode(header[6:]).decode('utf-8')
    planb = plain.split(":")
    user = Users.query.filter_by(userName=planb[0], password=planb[1]).first()
    if planb[0] in user.userName and planb[1] in user.password:
        borrow = Borrow.query.filter_by(borrowId=id).first_or_404()
        if 'borrowStatus' in data:
            borrow.returnDate = data['returnDate']
            borrow.borrowStatus = data['borrowStatus']
            db.session.commit()
            if borrow.borrowStatus:
                return {
                    'borrow id': borrow.borrowId, 
					'taken date': borrow.takenDate,
                    'brought date': borrow.broughtDate, 
					'return date': borrow.returnDate,
                    'book': {
                        'book code': borrow.book.bookID,
                        'book e': borrow.book.title,
                        'author': borrow.book.author,
                        'publisher': borrow.book.publisher
                    },
                    'borrower': {
                        'user id': borrow.borrower.userId,
                        'name': borrow.borrower.userName,
                        'email': borrow.borrower.email
                    },
                    'message': 'book return is successful'
                }, 201
            else:
                return {'error': 'wrong status'}


@app.route('/borrow/books/<id>/')
def get_borrowbook(id):
    bb = Borrow.query.filter_by(userId=id)
    return jsonify([
        {
            'book code': borrow.book.bookID,
            'book title': borrow.book.title,
            'author': borrow.book.author,
            'publisher': borrow.book.publisher,
        } for borrow in (bb)
    ])

@app.route('/borrow/users/<id>/')
def get_borrowuser(id):
    bb = Borrow.query.filter_by(bookID=id)
    return jsonify([
        {
            'user id': borrow.borrower.userId,
            'user name': borrow.borrower.userName,
            'email': borrow.borrower.email
        } for borrow in (bb)
    ])

###############################################################

@app.route('/books/')
def get_book():
    return jsonify([
        {
            'bookId': book.bookId, 
			'title': book.title, 
			'author': book.author,
            'publisher': book.publisher, 
			'copies': book.copies
        } for book in Book.query.all()
    ])

@app.route('/books/<id>/')
def show_book(id):
    book = Book.query.filter_by(bookID=id).first_or_404()
    return {
        'bookId': book.bookId, 
		'title': book.title, 
		'author': book.author,
		'publisher': book.publisher, 
		'copies': book.copies
    }

@app.route('/books/', methods=['POST'])
def add_book():
    data = request.get_json()
    if not 'title' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Book Title not given'
        }), 400
    book = Book(
            title = data['title'],
            author = data['author'],
            publisher = data['publisher'],
            copies = data['copies']
        )
    db.session.add(book)
    db.session.commit()
    return {
        'bookId': book.bookId, 
		'title': book.title, 
		'author': book.author,
        'publisher': book.publisher, 
		'copies': book.copies
    }, 201

@app.route('/books/<id>/', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    if not 'title' in data and not 'author' in data and not 'publisher' in data and not 'genres' in data and not 'copies' in data:
        return {
            'error': 'Bad Request',
            'message': 'field needs to be present'
        }, 400
    book = Book.query.filter_by(bookId=id).first_or_404()
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'publisher' in data:
        book.publisher = data['publisher']
    if 'copies' in data:
        book.copies = data['copies']
    db.session.commit()
    return jsonify({
        'success': 'data has been changed successfully',
        'bookId': book.bookId, 
		'title': book.title, 
		'author': book.author,
        'publisher': book.publisher, 
		'copies': book.copies
    })

@app.route('/books/<id>/', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(bookId=id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }

if __name__ =="__main__":
    app.run(debug=True)
