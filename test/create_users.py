from flask_server import db
from flask_server import Users

db.create_all() 
db.session.add(Users("user1", "123"))
db.session.add(Users("user2", "1234"))
db.session.add(Users("user3", "12345"))
db.session.add(Users("user4", "123456"))
db.session.add(Users("user5", "1234567")) 
db.session.commit()