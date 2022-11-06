from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    #email omitted from User class to allow for use of sql.alchemy user based functions
    def __init__(self, id, password):
        self.id=id
        self.set_password(password)

    def toJSON(self):
        return{
            'id': self.id,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Student(User):
    sid = db.Column(db.Integer, primary_key=True)
    studID = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    studemail=db.Column(db.String, nullable=False)
    courseR1 = db.Column(db.String(120), nullable=False)
    courseR2 = db.Column(db.String(120), nullable=False)
    courseR3 = db.Column(db.String(120), nullable=False)
    courseR4 = db.Column(db.String(120), nullable=False)
    courseR5 = db.Column(db.String(120), nullable=True)
    user = db.relationship('User')
    
    def __init__(self, studID, studemail, password, courseR1,courseR2,courseR3,courseR4,courseR5):
        super(Student, self).__init__(studID, password)
        self.studID=studID
        self.studemail = studemail
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
    staffemail=db.Column(db.String, nullable=False)
    course1 = db.Column(db.String(120), nullable=False)
    course2 = db.Column(db.String(120), nullable=False)
    course3 = db.Column(db.String(120), nullable=False)
    user = db.relationship('User')

    def __init__(self, staffID, staffemail, password ,course1,course2,course3):
        super(Staff, self).__init__(staffID, password)
        self.staffID=staffID
        self.staffemail = staffemail
        self.set_password(password)
        self.course1=course1
        self.course2=course2
        self.course3=course3

    def toJSON(self):
        return{
            'id': self.staffID,
            'email': self.staffemail,
            'course1' : self.course1,
            'course2' : self.course2,
            'course3' : self.course3,
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

    def toJSON(self):
        return{
            'id': self.recomID,
            'title': self.title,
            'description' : self.description,
            'course' : self.course,
            'comments' : self.comments,
            'status' : self.status
        }