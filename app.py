import os, jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
def create_app():
    db.init_app(app)
    db.create_all()
    return app


app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:admin@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

import view

if __name__ =="__main__":
	app.run(debug=True)
