# Python flask web server 
### Installation 
Download flask_server.py file from src/ to your project folder
###  Usage
First of all you need to change the following row based on your postgresql settings
``` python

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://<username>:<password>@localhost:<port>/<db_name>"

```
You can use flask_server.py in 2 ways. The first option is to run this file in your IDE or in command line using the following command(do not forget to install required packages in your virtual environment):
``` python

python flask_server.py

```
Now you can open your browser or requests making program and make requests. It has 3 routes:
- /sign_up (post and get)
- /login (post and get)
- /protected (use token as parameter)

The second option is a database managing without running a local server.
``` python
>>> from flask_server import db
>>> from task.flask_server import Users
```
Look at the Users model below, which has id, username, password and token fields. Username and token fields are unique. The constructor accepts only username and password.
``` python
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(200), unique=True, nullable=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username
```


### Examples
``` python
>>> db.create_all()   # creates tables in psql based on models

>>> username = "example_user" 
>>> password = "123" 

>>> user = Users(username, password) # creates a user 

>>> db.session.add(user) 
>>> db.session.commit()   # adds this row to psql users table

>>> Users.query.all()      
[<User 'asdfg'>, <User 'asdfwer'>, <User 'asdf'>, <User 'asdgas'>, <User 'example_user'>]

>>> Users.query.filter_by(username = "example_user").first()
<User 'example_user'>

>>> check_user = Users.query.filter_by(username = "example_user").first()
>>> print ("username: " + check_user.username + "\npassword: " + check_user.password) 
username: example_user
password: 123

```

