from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:230801@localhost:5432/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'thisismyflasksecretkey'

db = SQLAlchemy(app)

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

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
                
        if request.form['password'] == '' or request.form['username'] == '':
            return "<h1>Username or password fields might be empty!<h1>"

        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username= username).first()

        if user:
            if user.password == password:
                token = jwt.encode({'user':username, 'exp':datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
                user.token = token
                db.session.add(user)
                db.session.commit()
                return make_response('<h1> Token: '+ token + '</h1>')
            else:
                return make_response("<h1>Wrong password</h1>")
        else:
            return make_response("<h1>Could not found a user wiht login: " + username + "</h1>")

    elif request.method == 'GET':
        return '''
        <form method="post" align='center'>
            <h3>Log in</h3>
            <label>Username:<br><input type=text name=username></label><br><br>
            <label>Password:<br><input type=password name=password></label><br><br>
            <p><input type=submit value=Submit>
        </form>
        '''


@app.route("/sign_up", methods = ['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        error=""
        if request.form['password1'] == '' or request.form['username'] == '':
            error += "<h1>Username or password fields might be empty!<h1>"

        if Users.query.filter_by(username = request.form['username']).first():
            error += "<h1>This username already exists!<h1>"

        if (request.form['password1'] != request.form['password2']):
            error += "<h1>Passwords do not match!<h1>"

        if error != "":
            return error
        
        username = request.form['username']
        password = request.form['password1']
        token = jwt.encode({'user':username, 'exp':datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])

        user = Users(username, password)
        user.token = token
        db.session.add(user)
        db.session.commit()
        return "<h1>User " + username + " created!</h1>" + "<h1>Token: " + token + "</h1>"

    elif request.method == 'GET':
        return '''
        <form method="post" align='center'>
            <h3>Sign up</h3>
            <label>Username:<br><input type=text name=username></label><br><br>
            <label>Password:<br><input type=password name=password1></label><br><br>
            <label>Password confirmation:<br><input type=password name=password2></label><br><br>
            <p><input type=submit value=Submit>
        </form>
        '''


@app.route("/protected")
def protected():
    token = request.args.get('token')
    db_token = Users.query.filter_by(token=token).first()
    if (db_token):
        return make_response("<h1>Hello, token which is provided is correct</h1>")
    else:
        return make_response("<h1>Hello, could not verify the token</h1>")

if __name__ == '__main__':
    app.run(debug=True)