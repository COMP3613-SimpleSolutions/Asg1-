from App.models import Recommendation
from App.database import db

def create_recom(title, description, course,comments,status):
    newrecom = Recommendation(title=title, description = description, course = course,comments = comments,status=status)
    db.session.add(newrecom)
    db.session.commit()
    return newrecom

def accept_recom(recomid,comments):
    recom = Recommendation.query.filter_by(recomID=recomid).first()
    if recom:
        recom.status = "accepted"
        if comments:
            recom.comments = comments
        db.session.add(recom)
        return db.session.commit()
    return None

def reject_recom(recomid,comments):
    recom = Recommendation.query.filter_by(recomID=recomid).first()
    if recom:
        recom.status = "rejected"
        if comments:
            recom.comments = comments
        db.session.add(recom)
        return db.session.commit()
    return None

def load_recoms_bycourse(course):
    recomlist = []
    recoms = Recommendation.query.filter_by(course=data['course']).all()

    if recoms :
        recomlist = [Recommendation.toJSON(recom) for recom in recoms]
        return recomlist
    else:
        return None
