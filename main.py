from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text
import base64
import uuid

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@localhost:5432/perpus'
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

#################################################################################################

class Userz(db.Model):
    user_id = db.Column(db.Integer, primary_key = True, index =True)
    full_name = db.Column(db.String(45), nullable = False)
    user_name = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(45), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    is_admin = db.Column(db.Boolean, default = False)
    # phone = db.Column(db.String(15), nullable=False, unique=True)
    # address = db.Column(db.String(50), nullable=False)
    rent_user = db.relationship('Administration', backref = 'renter', lazy = 'dynamic')

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key = True, index = True)
    book_name = db.Column(db.String(45), nullable = False)
    release_year = db.Column(db.String(10), nullable = False)
    book_author = db.Column(db.String(45), nullable = False)
    publisher = db.Column(db.String(45), nullable = False)
    book_count = db.Column(db.Integer, nullable = False, default = 1)
    rent_book = db.relationship('Administration', backref = 'bbookk', lazy = 'dynamic')

class Administration(db.Model):
    booking_id = db.Column(db.Integer, primary_key = True, index = True)
    rent_date = db.Column(db.String(25), nullable = False)
    rent_due = db.Column(db.String(25), nullable = False)
    is_returned = db.Column(db.Boolean, default = False)
    return_date = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey('userz.user_id'), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable = False)

#################################################################################################

def get_user_data(id):
    return Userz.query.filter_by(user_id=id).first_or_404()

def get_book_data(id):
    return Book.query.filter_by(book_id=id).first_or_404()

def get_rent_data(id):
    return Administration.query.filter_by(booking_id=id).first_or_404()

def authz():
    token = request.headers.get('Authorization')
    token2 = token.replace("Basic ","")
    plain = base64.b64decode(token2).decode('utf-8')
    plain3 = plain.split(":")
    user = Userz.query.filter_by(user_name=plain3[0]).first()
    a = False
    if user is None :
        return a
    else: 
        hashcheck = bcrypt.check_password_hash(user.password, plain3[1])
        return hashcheck

def get_auth(user_name, password):
    return Userz.query.filter_by(user_name=user_name, password=password).first()

def return_user(u):
    return {
        'user id' : u.user_id,
        'username':u.user_name,
        'full name':u.full_name, 
        'email' : u.email, 
        'is admin': u.is_admin,
        # 'phone': u.phone,
        # 'address': u.address
            }

def return_book(b):
    return {'book id' : b.book_id,
    'book name':b.book_name, 
    'author': b.book_author,
    'release year' : b.release_year, 
    'publisher' : b.publisher, 
    'stock' : b.book_count}

def return_rent(rent):
    return {"1 Booking Information":{
                'Booking id': rent.booking_id, 
                'Rent date':rent.rent_date, 
                'Rent due': rent.rent_due, 
                'Is returned': rent.is_returned, 
                'Return date':rent.return_date, 
            },
            '2 Renter Information':{  
                'Name':rent.renter.full_name, 
                'Email': rent.renter.email, 
                'User id': rent.renter.user_id,
                # 'phone': rent.renter.phone, 
                # 'address': rent.renter.address
                }, 
            '3 Book Information':{ 
                'Book id': rent.bbookk.book_id, 
                'Book name': rent.bbookk.book_name, 
                'Release year': rent.bbookk.release_year, 
                'Book Author': rent.bbookk.book_author, 
                'Book Publisher': rent.bbookk.publisher
            }
        }

def get_hash(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def count_stock(book_id):
    qry = Administration.query.filter_by(is_returned=False, book_id=book_id).count()
    return qry

#################################################################################################

@app.route('/users/')
def get_users():
    return jsonify([return_user(user) for user in Userz.query.all()
    ])

@app.route('/books/')
def get_books():
    return jsonify([
        return_book(book) for book in Book.query.all()
    ])

@app.route('/users/<id>/')
def get_user(id):
    user = get_user_data(id)
    return return_user(user)

@app.route('/books/<id>/')
def get_book(id):
    book = get_book_data(id)
    return return_book(book)

@app.route('/users/',methods=['POST'])
def create_user():
    data = request.get_json()
    if (not 'user_name' in data) or (not 'email' in data) or (not 'full_name' in data):
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Username, Full name or Email is not given'
        }), 400
    if len(data['user_name']) < 4 or len(data['email']) < 6:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Username and Email must contain a minimum of 4 and 6 letters respectively'
        }), 400
    hash = get_hash(data['password'])
    u = Userz(
            user_name= data['user_name'],
            full_name= data['full_name'],
            email= data['email'],
            is_admin= data.get('is admin', False),
            # phone= data['phone'],
			# address= data['address'],
            password= hash
        )
    db.session.add(u)
    db.session.commit()
    return  return_user(u), 201

@app.route('/books/',methods=['POST'])
def create_book():
    data = request.get_json()
    if not 'book_name' in data or not 'year' or not 'author' or not 'publisher' or not 'stock' in data:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'One or more of the following field is empty: book_name, year, author, publisher, stock'
        }), 400
    if len(data['book_name']) < 4:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Book Name must contain a minimum of 4 letters'
        }), 400
    b = Book(
            book_name= data['book_name'], 
            release_year= data['year'], 
            book_author= data['author'],
            publisher= data['publisher'], 
            book_count= data['stock']
        )
    db.session.add(b)
    db.session.commit()
    return  return_book(b), 201

@app.route('/users/<id>/',methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = get_user_data(id)
    if 'user_name' in data:
        user.user_name=data['user_name']
    if 'full_name' in data:
        user.full_name=data['full_name']
    if 'email' in data:
        user.email=data['email']
    if 'is admin' in data:
        user.is_admin=data['is admin']
    # if 'phone' in data:
    #     user.phone=data['phone']
    # if 'address' in data:
    #     user.address=data['address']
    db.session.commit()
    return jsonify({'Success': 'User data has been updated'}, return_user(user))

@app.route('/books/<id>/',methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = get_book_data(id)
    if 'book_name' in data:
        book.book_name=data['book_name']
    if 'year' in data:
        book.release_year=data['year']
    if 'author' in data:
        book.book_author=data['author']
    if 'publisher' in data:
        book.publisher=data['publisher']
    if 'stock' in data:
        book.book_count=data['stock']
    db.session.commit()    
    return jsonify({'Success': 'Book data has been updated'}, return_book(book))

@app.route('/users/<id>/',methods=['DELETE'])
def delete_user(id):
    user = Userz.query.filter_by(user_id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return {
        'success': 'User data deleted successfully'
    }

@app.route('/books/<id>/',methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(book_id=id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    return {
        'success': 'Book data deleted successfully'
    }

#################################################################################################

@app.route('/rents/', methods=['GET'])
def get_rents():
    login = authz()
    if login:
        return jsonify([return_rent(rent) for rent in Administration.query.all()])
    else: return {"Error":"Wrong Username or Password"}

@app.route('/rents/<id>/', methods=['GET'])
def get_rent(id):
    login = authz()
    if login:
        rent = get_rent_data(id)
        user = get_user_data(id)
        return jsonify([return_rent(rent)])
    else: return {"Error":"Wrong Username or Password"}

@app.route('/rents/users/<id>', methods=['GET'])
def get_rent_users(id):
    login = authz()
    if login:
        rent = Administration.query.filter_by(user_id=id)
        return jsonify([
            {
                "Book Name" : x.bbookk.book_name,
                "Renter Name" : x.renter.full_name,
                "Rent Date" : x.rent_date,
                "Rent Due" : x.rent_due
                 
            }for x in rent
        ])

@app.route('/rents/books/<id>', methods=['GET'])
def get_rent_books(id):
    login = authz()
    if login:
        rent = Administration.query.filter_by(book_id=id)
        return jsonify([
            {
                "Book Name" : z.bbookk.book_name,
                "User Name" : z.renter.full_name,
                "Rent Date" : z.rent_date,
                "Rent Due" : z.rent_due,
                "Is returned" : z.is_returned
                 
            }for z in rent
        ])

@app.route('/rents/',methods=['POST']) # PEMINJAMAN
def create_rent():
    data=request.get_json()
    login = authz()
    if login:
        book = Book.query.filter_by(book_id=data['book_id']).first()
        book_count = count_stock(book.book_id)
        if book_count == book.book_count:
            return {"Error":"Sorry, this book has been rented out, please wait"}
        else :
            is_returned = data.get('is returned', False)
            # book = Book
            rent = Administration(
                rent_date = data['rent date'], rent_due = data['rent due'], user_id=data['user_id'], 
                book_id=data['book_id'], is_returned=is_returned
            )
            db.session.add(rent)
            db.session.commit()    
            return jsonify([{"Success": "Rent data has been saved"}, return_rent(rent)]), 201 
    else: return {"Error":"Wrong Username or Password"}

@app.route('/rents/<id>/',methods={'PUT'}) # PENGEMBALIAN
def update_rent(id):
    data = request.get_json()
    login = authz()
    if login:
        rent = get_rent_data(id)
        if 'rent date' in data:
            rent.rent_date = data.get('rent date', rent.rent_date)
        if 'rent due' in data:
            rent.rent_due = data.get('rent due', rent.rent_due)
        if 'is returned' in data:
            rent.is_returned=data['is returned']
            if rent.is_returned:
                rent.return_date = data['return date']
        db.session.commit() 
        return jsonify([{"Success": "Rent data has been updated"}, return_rent(rent)]), 201 
    else: return {"Error":"Wrong Username or Password"}

@app.route('/rents/<id>/', methods=['DELETE'])
def delete_rent(id):
    login = authz()
    if login:
        rent = Administration.query.filter_by(booking_id=id).first_or_404()
        # Book(book_count+=1)
        db.session.delete(rent)
        db.session.commit()
        return {
            'success': 'Rent data deleted successfully'
        }  
    else: return {"Error":"Wrong Username or Password"}