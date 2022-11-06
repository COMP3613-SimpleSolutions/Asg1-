from App.models import User, Student, Staff
from App.database import db
from flask_login import current_user


def create_student(studid, email, password, course1, course2, course3, course4, course5):
    newstudent = Student(studID=studid,studemail=email,password=password,courseR1=course1,courseR2=course2,courseR3=course3,courseR4=course4,courseR5=course5)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def create_staff(staffid, email, password, course1, course2, course3):
    newstaff = Staff(staffID=staffid,staffemail=email,password=password,course1=course1,course2=course2,course3=course3)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None


    