from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email =  db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __init__(self, id, email, password):
        self.id=id
        self.email = email
        self.set_password(password)

    def toJSON(self):
        return{
            'user id': self.id,
            'email': self.email,
        }

    #def get_id(self):
     #      return (self.userID)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Student(User):
    id = db.Column(db.Integer, primary_key=True)
    studID = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    courseR1 = db.Column(db.String(120), nullable=False)
    courseR2 = db.Column(db.String(120), nullable=False)
    courseR3 = db.Column(db.String(120), nullable=False)
    courseR4 = db.Column(db.String(120), nullable=False)
    courseR5 = db.Column(db.String(120), nullable=True)
    user = db.relationship('User')
    
    def __init__(self, studID, email, password, courseR1,courseR2,courseR3,courseR4,courseR5):
        super(Student, self).__init__(studID, email, password)
        self.studID=studID
        self.email = email
        self.set_password(password)
        self.courseR1=courseR1
        self.courseR2=courseR2
        self.courseR3=courseR3
        self.courseR4=courseR4
        self.courseR5=courseR5

    def toJSON(self):
        return{
            'id': self.studID,
            'course1' : self.courseR1,
            'course2' : self.courseR2,
            'course3' : self.courseR3,
            'course4' : self.courseR4,
            'course5' : self.courseR5,
        }

class Staff(User):
    staffID = db.Column(db.Integer,  db.ForeignKey('user.id') ,primary_key=True)
    course1 = db.Column(db.String(120), nullable=False)
    course2 = db.Column(db.String(120), nullable=False)
    course3 = db.Column(db.String(120), nullable=False)
    user = db.relationship('User')

    def __init__(self, staffID, email, password ,course1,course2,course3):
        super(Staff, self).__init__(staffID, email, password)
        self.staffID=staffID
        self.email = email
        self.set_password(password)
        self.course1=course1
        self.course2=course2
        self.course3=course3

    def toJSON(self):
        return{
            'id': self.staffID,
            'username': self.email
        }


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