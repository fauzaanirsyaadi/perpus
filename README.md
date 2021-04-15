Cars in a Flask
This repository contains the code for this blogpost.

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
$ cd cars_in_a_flask

2. With Python 3.6 and Pip installed:
$ virtualenv --python=python3 env --no-site-packages
$ source env/bin/activate
$ pip install -r requirements.txt

3. Create a PostgreSQL user with the username and password postgres and create a database called library:

$ createuser --interactive --pwprompt
$ createdb (dabase_name)

4. Export the required environment variables:
$ export FLASK_APP=app.py

5. Execute the migrations to create the cars table:
$ flask db migrate
$ flask db upgrade

6. Run the Flask API:
$ flask run
Navigate to http://localhost:5000/ to view the data.