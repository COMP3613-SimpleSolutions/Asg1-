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
    recomlist=[]
    data = request.json

    if data:
        recoms = Recommendation.query.filter_by(course=data['course']).all()

        if recoms :
            recomlist = [Recommendation.toJSON for recom in recoms]
            return jsonify(recomList)

        else:
            return jsonify({"message":"No recommendations found"})
    else:
        return jsonify({"message":"No recommendations found"})