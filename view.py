from flask import jsonify, request, redirect
import uuid, jwt
from  app import app, db, token_required, admin_required
from models import User, Book, Borrow
import base64

@app.route('/')
def home():
	return {
		'message': 'halo dunia '
	}

# @app.route('/user/')
# # @token_required
# # @admin_required
# def get_users(current_user):
# 	return jsonify([
# 		user.get_json() for user in User.query.all()
# 	])

@app.route('/users/')
def get_users():
    return jsonify([
        {
            'userId': user.userId, 
			'name': user.userName, 
			'email': user.email,
			'phone': user.phone,
			'address': user.address
        } for user in User.query.all()
    ])
		
# @app.route('/user/me/')
# # @token_required
# def get_user(current_user: User):
# 	return current_user.get_json()

@app.route('/users/<id>/')
def get_user(id):
    print(id)
    user = User.query.filter_by(userId=id).first_or_404()
    return {
        'userId': user.userId,
		'name': user.userName, 
		'email': user.email,
		'password': user.password,
		'address':user.address,
		'phone':user.phone
    }

@app.route('/user/', methods=['POST'])
def create_user():
	data = request.get_json()
	if not 'userName' in data or not 'email' in data or 'password' not in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name, email or password not given'
		}), 400
	if len(data['userName']) < 4 or len(data['email']) < 6:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name and email must be contain minimum of 4 letters'
		}), 400
	u = User(
			userName=data['userName'], 
			email=data['email'],
			phone=data['phone'],
			address=data['address'],
			is_admin=data.get('is admin', False),
			public_id=str(uuid.uuid4())
		)
	u.set_password(data['password'])
	db.session.add(u)
	db.session.commit()
	# return u.get_json(), 201
	return {
        'userId': u.userId, 'userName': u.userName, 'email': u.email
    }, 201

# @app.route('/user/token/', methods=['POST'])
# def get_token():
# 	try:
# 		data = request.get_json()
# 		if 'email' not in data or 'password' not in data:
# 				return {
# 						'error': 'Invalid data',
# 						'message': 'email and password must be present.'
# 				}, 400
# 		u = User.query.filter_by(email=data['email']).first()
# 		if not u or not u.check_password(data['password']):
# 				return {
# 						'error': 'Invalid Data',
# 						'message': 'invalid email or password'
# 				}, 401
# 		try:
# 			token = jwt.encode(
# 				{'userId': str(u.id)},
# 				app.config['SECRET_KEY']
# 			)
# 			return {
# 					'token': token
# 			}, 200
# 		except Exception as e:
# 			return {
# 				'error': 'Sonething went wrong',
# 				'message': str(e)
# 			}, 500
# 	except Exception as e:
# 		return {
# 			'error': 'Bad data',
# 			'message': str(e)
# 		}, 400 

# @app.route('/user/', methods=['PUT'])
# @token_required
# def update_user(current_user):
# 	data = request.get_json()
# 	current_user.userName=data.get('userName', current_user.userName)
# 	if 'admin' in data:
# 		current_user.is_admin=data['admin']
# 	db.session.commit()
# 	return jsonify(current_user.get_json())

@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    if not 'userName' in data and not 'email' in data and not 'password' in data:
        return {
            'error': 'Bad Request',
            'message': 'field needs to be present'
        }, 400
    user = User.query.filter_by(userId=id).first_or_404()
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
		# 'phone': user.phone,
		# 'address': user.address
    })

# @app.route('/user/', methods=['DELETE'] )
# @token_required
# def delete_user(current_user):
# 	db.session.delete(current_user)
# 	db.session.commit()
# 	return {
# 		'success': 'User deleted successfully'
# 	}

@app.route('/users/<id>/', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(userId=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }

# @app.route('/users/borrow/')
# @token_required
# @admin_required
# def get_borrow(current_user):
# 	return jsonify([
# 		borrow.get_json() for borrow in Borrow.query.all()
# 	])

##########################################################

@app.route('/borrow/')
def get_borrow():
    header = request.headers.get('authorization')
    plain = base64.b64decode(header[6:]).decode('utf-8')
    planb = plain.split(":")
    user = User.query.filter_by(name=planb[0], password=planb[1]).first_or_404()
    if planb[0] in user.name and planb[1] in user.password:
        return jsonify([
            {
                'book': {
                    'book code': borrow.books.bookID,
                    'book title': borrow.book.title,
                    'author': borrow.book.author,
                    'publisher': borrow.book.publisher
                },
                'Borrow id': borrow.borrowId, 
				'start date': borrow.takenDate,
                'end date': borrow.broughtDate,
                'borrower': {
                    'user id': borrow.borrower.userId,
                    'name': borrow.borrower.userName,
                    'email': borrow.borrower.email,
					'phone': borrow.borrower.phone
                }
            } for borrow in Borrow.query.all()
        ])

# @app.route('/user/borrow/<id>/')
# @token_required
# def get_borrow(current_user, id):
	# borrow: Borrow = Borrow.query.filter_by(public_id=id).first_or_404()
	# if current_user != borrow.borrower or not borrow.borrower.is_admin:
	# 	return {
	# 		'error': 'Forbidden',
	# 		'message': 'You don\'t have access and you are not an admin'
	# 	}, 403
	# return jsonify(borrow.get_json())

# @app.route('/user/borrow/', methods=['POST'])
# @token_required
# def create_borrow(current_user: User):
# 	data = request.get_json()
# 	if not 'userName' in data:
# 		return jsonify({
# 			'error': 'Bad Request',
# 			'message': 'Name of borrower not given'
# 		}), 400
# 	if len(data['userName']) < 4:
# 		return jsonify({
# 			'error': 'Bad Request',
# 			'message': 'Name of borrower contain minimum of 4 letters'
# 		}), 400

# 	is_completed = data.get('is completed', False)
# 	borrow = Borrow(
# 		userName=data['userName'], 
# 		userId=current_user.id,
# 		is_completed=is_completed, 
# 		public_id=str(uuid.uuid4())
# 	)
# 	db.session.add(borrow)
# 	db.session.commit()
# 	return borrow.get_json(), 201

@app.route('/borrow/', methods=['POST'])
def add_borrow():
    data = request.get_json()
    header = request.headers.get('authorization')
    plain = base64.b64decode(header[6:]).decode('utf-8')
    planb = plain.split(":")
    user = User.query.filter_by(userName=planb[0], password=planb[1]).first_or_404()
    book = Book.query.filter_by(bookID=data['bookID']).first()
    count = Borrow.query.filter_by(borrowStatus=False, bookID=data['bookID']).count()
    if planb[0] in user.userName and planb[1] in user.password:
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

# @app.route('/user/borrow/<id>/', methods=['PUT'])
# @token_required
# def update_borrow(current_user, id):
# 	data = request.get_json()
# 	if not data.get('userName') and not  data.get('completed'):
# 		return {
# 			'error': 'Bad Request',
# 			'message': 'Name or completed fields need to be present'
# 		}, 400
# 	borrow = Borrow.query.filter_by(public_id=id).first_or_404()
# 	if current_user != borrow.borrower:
# 		return {
# 			'error': 'Forbidden',
# 			'message': 'You don\'t have access'
# 		}, 403
# 	borrow.userName=data.get('userName', borrow.userName)
# 	borrow.is_completed=data.get('completed', False)
# 	db.session.commit()
# 	return borrow.get_json(), 201

# @app.route('/user/borrow/<id>/', methods=['DELETE'] )
# @token_required
# def delete_borrow(current_user, id):
# 	borrow = Borrow.query.filter_by(public_id=id).first_or_404()
# 	if current_user != borrow.borrower:
# 		return {
# 			'error': 'Forbidden',
# 			'message': 'You don\'t have access'
# 		}, 403
# 	db.session.delete(borrow)
# 	db.session.commit()
# 	return {
# 		'success': 'Data deleted successfully'
# 	}

app.route('/borrow/<id>/', methods=['PUT'])
def return_borrow(id):
    data = request.get_json()
    header = request.headers.get('authorization')
    plain = base64.b64decode(header[6:]).decode('utf-8')
    planb = plain.split(":")
    user = User.query.filter_by(userName=planb[0], password=planb[1]).first()
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
def get_book(id):
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