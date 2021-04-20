Getting Started
Prerequisites
Kindly ensure you have the following installed:

Python 3.6
Pip
Virtualenv
PostgreSQL

Setting up + Running
1. Clone the repo:

$ git clone https://github.com/(user)/(repository).git
$ cd folder-name

2. With Python 3.6 and Pip installed

$ pip install virtualenv
$ virtualenv env 
$ env\Scripts\activate.bat
$ pip install -r requirements.txt

to stop 
$ deactive

3. Create a PostgreSQL user with the username and password postgres and create a database called library:

$ createuser --interactive --pwprompt
$ createdb (dabase_name)

4. Export the required environment variables:
$ export FLASK_APP=app.py
$env:FLASK_APP = "app.py"
or
set FLASK_APP=main.py


1. Execute the migrations to create the table:
$ flask db init
$ flask db migrate
$ flask db upgrade

6. Run the Flask API:
$ flask run
Navigate to http://localhost:5000/ to view the data.

7. DB
flask shell
from main import db, Userz, Administration, Book
db.create_all()