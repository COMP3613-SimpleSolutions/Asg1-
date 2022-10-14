from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import User, Staff, Student, Recommendation

from App.database import db

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/make', methods=['POST'])
def makeRecom_action():
    data = request.json
    newrec = Recommendation(title=data['recomTitle'], description=data['recomDesc'], course=data['course'], comments=None, status="unchecked")
    
    db.session.add(newrec)
    db.session.commit()
    return jsonify({"message":f" {data['recomTitle']} recommendation created "})

@index_views.route('/view', methods=['GET'])
def loadrecoms():
    data = request.json
    recomlist=[]  

    recoms = Recommendation.query.filter_by(course=data['course']).all()

    if recoms :
        recomlist = [Recommendation.toJSON(recom) for recom in recoms]
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
    data = request.json

    recom = Recommendation.query.filter_by(recomID=recomid).first()

    if recom :
        if data:
            recom.comments=data["comments"]
        recom.status = "accepted"
        recom=recom.toJSON()
        return jsonify(recom)

    else:
        return jsonify({"message":"No recommendations found"})

@index_views.route('/view/<recomid>/reject', methods=['POST'])
def rejectrecom(recomid):
    data = request.json 

    recom = Recommendation.query.filter_by(recomID=recomid).first()

    if recom :
        recom.comments=data["comments"]
        recom.status = "rejected"
        recom=recom.toJSON()
        return jsonify(recom)

    else:
        return jsonify({"message":"No recommendations found"})

@index_views.route('/notifs', methods=['GET'])
def loadnotifs():
    data = request.json
    recomlist=[]  
    if data:
        staff = Staff.query.filter_by(recomID=data['staffID']).first()

        if staff:
            staffsubs = [staff.course1,staff.course2,staff.course3]
            if staffsubs :
                for sub in staffsubs:
                    recoms = Recommendation.query.filter_by(course=sub).all()
                if recoms:
                    for recom in recoms:
                        if recom.status == "unchecked":
                            recomlist.append(recom)
                    return jsonify(recomlist.toJSON)

        else:
            return jsonify({"message":"No recommendations found"})
    else:
        return jsonify({"message":"No recommendations found"})