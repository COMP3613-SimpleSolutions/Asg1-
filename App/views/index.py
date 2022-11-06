from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import User, Staff, Student, Recommendation
from flask_login import  LoginManager, current_user, login_user, login_required
from App.controllers import (
    create_staff,
    create_student,
    create_recom,
    accept_recom,
    reject_recom,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user
)

from App.database import db

index_views = Blueprint('index_views', __name__, template_folder='../templates')

def loadstud(): #loads student courses
  student = Student.query.filter_by(studID=current_user.id).first()
  subs=[student.courseR1,student.courseR2,student.courseR3,student.courseR4,student.courseR5]
  return subs

def loadstaff(): #loads staff courses
  staff = Staff.query.filter_by(staffID=current_user.id).first()
  subs=[staff.course1,staff.course2,staff.course3]
  return subs

def isStud(): #determines if logged in user is a student or not
  if current_user.id >= 800000000:
    return True
  else:
    return False

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/login', methods=['POST'])
def login():
    data = request.json
    
    user = User.query.filter_by(id = data['userID']).first()
    if user:
        print("User exists")
    if user and user.check_password(data['password']):
        login_user(user) 
    
        return jsonify({"message":f"{data['userID']} logged in "})
    else:
        return jsonify({"message" :"Could not log in/ Incorrect credentials"})

@index_views.route('/loadusers',methods=['GET'])
def loadall():
    users = get_all_users_json()
    return jsonify(users)

@index_views.route('/make', methods=['POST'])
def makerecom_action():
    data = request.json

    if isStud() == True:
        newrec = Recommendation(title=data['recomTitle'], description=data['recomDesc'], course=data['course'], comments=None, status="unchecked")

        db.session.add(newrec)
        db.session.commit()
        return jsonify({"message":f" {data['recomTitle']} recommendation created "})
    else :
        return jsonigy({"message" : "User type cannot access this function"})

@index_views.route('/view', methods=['GET'])
def loadrecoms(): #function to load recommendations for a specific class
    data = request.json
    
    course = data['course']
    recomlist = load_recoms_bycourse(course)
    
    if recomlist:
        return jsonify(recomlist)

    else:
        return jsonify({"message":"No recommendations found"})

@index_views.route('/view/<recomid>', methods=['GET'])
def loadrecom(recomid):
    data = request.json
    recomlist=[]  

    recom = Recommendation.query.filter_by(recomID=data['recomID']).first()

    if recom :
        recom=recom.toJSON()
        return jsonify(recom)

    else:
        return jsonify({"message":"No recommendations found"})

@index_views.route('/view/<recomid>/accept', methods=['POST'])
def acceptrecom(recomid):
    if isStud() == False:
        data = request.json

        recom = Recommendation.query.filter_by(recomID=recomid).first()

        if recom :
            accept_recom(recom.recomID)
            recom=recom.toJSON()
            return jsonify(recom)

        else:
            return jsonify({"message":"No recommendations found"})
    else :
        return jsonigy({"message" : "User type cannot access this function"})

@index_views.route('/view/<recomid>/reject', methods=['POST'])
def rejectrecom(recomid):
    data = request.json

    if isStud() == False:
        recom = Recommendation.query.filter_by(recomID=recomid).first()

        if recom :
            reject_recom(recom.recomID)
            recom=recom.toJSON()
            return jsonify(recom)

        else:
            return jsonify({"message":"No recommendations found"})
    else :
        return jsonigy({"message" : "User type cannot access this function"})

@index_views.route('/notifs', methods=['GET'])
def loadnotifs():
    data = request.json

    if isStud() == False:
        recomlist=[]  
        if data:
            staff = Staff.query.filter_by(staffID=data['staffID']).first()

            if staff:
                staffsubs = [staff.course1,staff.course2,staff.course3]

                for sub in staffsubs:
                    recoms = Recommendation.query.filter_by(course=sub).all()
                    if recoms:
                        for recom in recoms:
                            if recom.status == "unchecked":
                                recomlist.append(recom)

                recomslist=[Recommendation.toJSON(Recommendation) for recom in recomlist]              
                return jsonify(recomslist)

            else:
                return jsonify({"message":"No recommendations found"})
        else:
            return jsonify({"message":"No recommendations found"})
    else :
        return jsonigy({"message" : "User type cannot access this function"})