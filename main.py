import os, uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import base64


app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy()

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@localhost:5432/perpus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    user_name = db.Column(db.String(50), nullable=False)
    password= db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    address = db.Column(db.String(50), nullable=False)
    borrow=db.relationship('Borrow', backref='borrower', lazy='dynamic') #untuk relasi
    #backref deklarasi propetis yang baru, lazy untuk menentukan kapan sqlalchemy akan memuat data dari DB 
    #declarasi properti dibawah class , Borrow

class Borrow(db.Model):
    borrow_id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)#mengikuti postgres auto kecil
    book_id=db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    taken_date= db.Column(db.String(30), nullable=False)
    brought_date= db.Column(db.String(30), nullable=False)
    return_date = db.Column(db.String(25), nullable=False)
    borrow_status = db.Column(db.Boolean, default=False)
    # ini sudah ada foreignkeys
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50))
    copies = db.Column(db.String(3), nullable=False)
    borrow_book = db.relationship('Borrow', backref='book', lazy='dynamic')####
    # backref=untuk relasi  lazy=

def auth():
    res = request.headers.get("Authorization") # ambil res, di postman pilih basic auth, tulis password dan email 
    a = res.split()
    u = base64.b64decode(a[-1]).decode('utf-8') # kita buang basic
    b = u.split(":")
    return b
    
def return_rent(rent):
    return {"1 Booking Information":{
                'Booking id': rent.booking_id, 
                'Rent date':rent.taken_date, 
                'Rent due': rent.brought_date, 
                'Return date':rent.return_date, 
            },
            '2 Renter Information':{  
                'Name':rent.borrower.full_name, 
                'Email': rent.borrower.email, 
                'User id': rent.borrower.user_id
                }, 
            '3 Book Information':{ 
                'Book id': rent.book.book_id, 
                'Book name': rent.book.book_name, 
                'Release year': rent.book.book_year, 
                'Book Author': rent.book.book_author
            }
        }
@app.route('/users/')
def get_users():

    return jsonify([
        {
            'user_id': user.user_id, 
			'name': user.user_name, 
			'email': user.email,
			'phone': user.phone,
			'address': user.address
            } for user in Users.query.all() #query dari data base = select * from Users
    ])
	
@app.route('/users/<id>/')
def get_user(id): #deklarasi fungsi
    print(id)
    user = Users.query.filter_by(user_id=id).first_or_404() # untuk jika return error
    return {
        'user_id': user.user_id,
		'name': user.user_name, 
		'email': user.email,
		'password': user.password,
		'address':user.address,
		'phone':user.phone
    }

@app.route('/users/', methods=['POST'])
def create_user():
	data = request.get_json() # ambil json (body)
	if (not 'user_name' in data) or (not 'email' in data) or (not 'password' in data):
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name, email or password not given'
		}), 400
	elif len(data['user_name']) < 4 or len(data['email']) < 6:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name and email must be contain minimum of 4 letters'
		}), 400
	else: 
            u = Users( #
                user_name=data['user_name'], 
                email=data['email'],
                password=data['password'],
                phone=data['phone'],
                address=data['address']
		)
	db.session.add(u) #untuk masuk  ke DB
	db.session.commit() # untuk masuk ke DB
	return {
        'user_id': u.user_id, 
        'user_name': u.user_name, 
        'email': u.email,
        'phone': u.phone,
        'address': u.address
    }, 201
 

@app.route('/login_users/', methods = ['POST'])
def login_users():
    data = request.get_json()
    if not 'email' in data and not 'password' in data:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Email or password must be given'
        }), 400
        
    if bcrypt.check_password_hash(Users.password, data["password"]):
        return jsonify ({
            'user_id': Users.user_id, 
            'name': Users.name, 
            'email': Users.email, 
            'password' : Users.password
        })
    else:
        return jsonify ({
            "message" : "Invalid email or password!"
        }), 401

   
@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    if not 'user_name' in data and not 'email' in data and not 'password' in data and not 'address' in data and not 'phone' in data:
        return {
            'error': 'Bad Request',
            'message': 'field needs to be present'
        }, 400

    user = Users.query.filter_by(user_id=id).first_or_404()
    if 'user_name' in data:
        user.user_name = data['user_name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
	# if 'phone' in data:
    #     user.phone = data['phone']
	# if 'address' in data:
    #     user.address = data['address']

    db.session.commit()
    return jsonify({
        'success': 'data has been changed successfully',
        'user_id': user.user_id, 'user_name': user.user_name, 'email': user.email
    })

@app.route('/users/<id>/', methods=['DELETE'])
def delete_user(id):
    user = Users.query.filter_by(user_id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }


###############################################################

@app.route('/books/')
def get_book():
    return jsonify([
        {
            'book_id': book.book_id, 
			'title': book.title, 
			'author': book.author,
            'publisher': book.publisher, 
			'copies': book.copies
        } for book in Book.query.all()
    ])

@app.route('/books/<id>/')
def show_book(id):
    book = Book.query.filter_by(book_id=id).first_or_404()
    return {
        'book_id': book.book_id, 
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
    if len(data['title']) < 1:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Title of book should contain minimum of 1 letter'
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
        'book_id': book.book_id, 
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
    book = Book.query.filter_by(book_id=id).first_or_404()
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
        'book_id': book.book_id, 
		'title': book.title, 
		'author': book.author,
        'publisher': book.publisher, 
		'copies': book.copies
    })

@app.route('/books/<id>/', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(book_id=id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }


##########################################################
#di sqlalchemy pakai backref, 
@app.route('/borrow/')
def get_borrow():
    login = auth()
    if login:
        return jsonify([ #bisa 
            {
                'transaction_id': borrow.transaction_id, 
                'user_id': borrow.user_id, 
                'book_id': borrow.book_id, 
                'checkout_date': borrow.checkout_date, 
                'return_date': borrow.return_date,
                'user' : {
                    "user_name": borrow.borrower.user_name, # dalam bisa nampilin isi dari user
                } # backref adalah after table name borrower adalah alias  
            } for borrow in Borrow.query.all() # for i in len(borrow)
        ]) #tidak perlu appent karena pakai jsonify
    else: return {"Error":"Wrong Username or Password"}# bisa

@app.route('/borrow/books/<id>/')
def get_borrowbook(id): 
    bb = Borrow.query.filter_by(user_id=id)
    login = auth()
    if login:
        return jsonify([
            {
                'book code': borrow.book.book_id,
                'book title': borrow.book.title,
                'author': borrow.book.author,
                'publisher': borrow.book.publisher,
            } for borrow in (bb)
        ])
    return {"Error":"Wrong Username or Password"}

def count_stock(book_id):
    query =  Borrow.query.filter_by(book_id=book_id).count()
    return query

@app.route('/borrow/', methods=['POST'])
def add_borrow():
    data=request.get_json()
    login = auth()
    if login:
        book = Book.query.filter_by(book_id=data['book_id']).first()
        book_count = count_stock(book.book_id)
        if book_count == book.book_count:
            return {"Error":"Sorry, this book has been rented out, please wait"}
        else :
            db.session.add(rent)
            db.session.commit()    
            return jsonify([{"Success": "Rent data has been saved"}, return_rent(rent)]), 201 
    else: return {"Error":"Wrong Username or Password"}

    
app.route('/borrow/<id>/', methods=['PUT'])
def return_borrow(id):
    data = request.get_json()
    header = request.headers.get('authorization')
    plain = base64.b64decode(header[6:]).decode('utf-8')
    planb = plain.split(":")
    user = Users.query.filter_by(user_name=planb[0], password=planb[1]).first()
    if planb[0] in user.user_name and planb[1] in user.password:
        borrow = Borrow.query.filter_by(borrow_id=id).first_or_404()
        if 'borrow_status' in data:
            borrow.return_date = data['return_date']
            borrow.borrow_status = data['borrow_status']
            db.session.commit()
            if borrow.borrow_status:
                return {
                    'borrow id': borrow.borrow_id, 
					'taken date': borrow.taken_date,
                    'brought date': borrow.brought_date, 
					'return date': borrow.return_date,
                    'book': {
                        'book code': borrow.book.book_id,
                        'book e': borrow.book.title,
                        'author': borrow.book.author,
                        'publisher': borrow.book.publisher
                    },
                    'borrower': {
                        'user id': borrow.borrower.user_id,
                        'name': borrow.borrower.user_name,
                        'email': borrow.borrower.email
                    },
                    'message': 'book return is successful'
                }, 201
            else:
                return {'error': 'wrong status'}

@app.route('/borrow/users/<id>/')
def get_borrowuser(id):
    bb = Borrow.query.filter_by(book_id=id)
    return jsonify([
        {
            'user id': borrow.borrower.user_id,
            'user name': borrow.borrower.user_name,
            'email': borrow.borrower.email
        } for borrow in (bb)
    ])

if __name__ =="__main__":
    app.run(debug=True)
