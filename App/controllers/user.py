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

def loadstud(): #loads student courses
  student = Student.query.filter_by(studID=current_user.userID).first()
  subs=[student.courseR1,student.courseR2,student.courseR3,student.courseR4,student.courseR5]
  return subs

def loadstaff(): #loads staff courses
  staff = Staff.query.filter_by(staffID=current_user.userID).first()
  subs=[staff.course1,staff.course2,staff.course3]
  return subs

def isStud(): #determines if logged in user is a student or not
  if current_user.userID >= 800000000:
    return True
  else:
    return False
    