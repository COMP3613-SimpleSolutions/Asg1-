import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User, Student, Staff
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        student = Student(816026077,"bob.saget@studmail.com","bobpass","COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
        assert student.studID == 816026077

    # pure function no side effects or integrations called
    def test_toJSON(self):
        student = Student(816026077,"bob.saget@studmail.com","bobpass","COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
        student_json = student.toJSON()
        self.assertDictEqual(student_json, {"id":816026077, "course1" : "COMP1600","course2" : "COMP1601","course3" : "COMP1602","course4" : "COMP1603","course5" : "COMP1604",})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        student = Student(816026077,"bob.saget@studmail.com",password,"COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
        assert student.password != password

    def test_check_password(self):
        password = "mypass"
        student = Student(816026077,"bob.saget@studmail.com",password,"COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
        assert student.check_password(password)

    def test_new_recommendation(self):
        recom = Recommendation("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        assert recom.title == "New Fan"
    
    def test_view_recommendation(self):
        recom = Recommendation("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        self.assertDictEqual(recom_json, {"id": None,"title": "New Fan","description" : "We need a new fan the class is too hot.","course" : "COMP1600","comments" : None,"status" : "unchecked"})

    def test_accept_recommendation(self):
        recom = Recommendation("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        recom.status = "accepted"
        recom_json = recom.toJSON()
        self.assertDictEqual(recom_json, {"id": None,"title": "New Fan","description" : "We need a new fan the class is too hot.","course" : "COMP1600","comments" : None,"status" : "accepted"})

    def test_reject_recommendation(self):
        recom = Recommendation("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        recom.status = "rejected"
        recom_json = recom.toJSON()
        self.assertDictEqual(recom_json, {"id": None,"title": "New Fan","description" : "We need a new fan the class is too hot.","course" : "COMP1600","comments" : None,"status" : "rejected"})
         
    def test_view_notifications(self):
        recomlist=[]
        recom1 = Recommendation("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        recom2 = Recommendation("New Desks","We need new desks for space.","COMP1601",None,"accepted")
        recoms = Recommendation.query.filter_by(status=unchecked).all()
        for recom in recoms:
            recomlist.append(recom.toJSON())
        self.assertDictEqual(recomlist, {"id": None,"title": "New Fan","description" : "We need a new fan the class is too hot.","course" : "COMP1600","comments" : None,"status" : "rejected"})
         

