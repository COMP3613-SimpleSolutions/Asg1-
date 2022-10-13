from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    userID = db.Column(db.Integer, primary_key=True)
    email =  db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __init__(self, userID, email, password):
        self.userID=userID
        self.email = email
        self.set_password(password)

    def toJSON(self):
        return{
            'user id': self.userID,
            'email': self.email,
        }

    def get_id(self):
           return (self.userID)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)




class Recommendation(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    recomID = db.Column(db.Integer,primary_key=True)
    title =  db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    course = db.Column(db.String(120), nullable=False)
    comments = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False)

    def __init__(self, title, description, course,comments,status):
        self.title = title
        self.description=description
        self.course=course
        self.comments=comments
        self.status=status