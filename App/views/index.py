from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/make', methods=['GET'])
def makeRecom_action():
    data = request.json
    #newrec = Recommendation(title=data['recomTitle'], description=data['recomDesc'], course=data['course'], comments=None, status="unchecked")
    return jsonify({"message": "hellow"})
    #db.session.add(newrec)
    #db.session.commit()
    #return jsonify({"message":f" {data['recomTitle']} recommendation created "})