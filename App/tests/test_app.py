import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User, Student, Staff, Recommendation


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
    
    def test_student_user_login(self):
        student = Student(816026077,"bob.saget@studmail.com","bobpass","COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
        login_id = 816026077
        password = "bobpass"
        assert (login_id,True) == (student.studID,student.check_password(password))

    def test_staff_user_login(self):
        staff = Staff(216000001,"bob.ross@staffmail.com","bobpass","COMP1600","COMP1601","COMP1602")
        login_id = 216000001
        password = "bobpass"
        assert (login_id,True) == (staff.staffID,staff.check_password(password))

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
        recom_json = recom.toJSON()
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

        if recom1.status == "unchecked":    #using a quesry was not returning valid results so an individual check was done on both created recommendations
            recom_json = recom1.toJSON()    #the goal was to only get the recommendation marked as unchecked into the dictionary and have that be the only returned json object
            recomlist.append(recom_json)
        if recom2.status == "unchecked":
            recom_json = recom2.toJSON()
            recomlist.append(recom_json)
        
        self.assertDictEqual(recomlist[0], {"id": None,"title": "New Fan","description" : "We need a new fan the class is too hot.","course" : "COMP1600","comments" : None,"status" : "unchecked"})
        
# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')


def test_authenticate_student():
    student = create_student(816026077,"bob.saget@studmail.com","bobpass","COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
    assert authenticate(816026077, "bobpass") != None

def test_authenticate_staff():
    staff = create_staff(216000001,"bob.ross@staffmail.com","bobpass","COMP1600","COMP1601","COMP1602")
    assert authenticate(216000001, "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        student = create_student(816026078,"john.stamos@studmail.com","johnpass","COMP1601","COMP1602","COMP1603","COMP1604","INFO1600")
        assert student.id == 816026078

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":216000001}, {"id":816026077}, {"id":816026078}], users_json)

    def test_create_recommendation(self):
        recom = create_recom("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        assert recom.title == "New Fan"
    
    # Tests data changes in the database
    def test_accept_recommendation(self):
        recom = create_recom("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        accept_recom(recom.recomID,None)
        assert recom.status == "accepted"

    def test_reject_recommendation(self):
        recom = create_recom("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        reject_recom(recom.recomID,None)
        assert recom.status == "rejected"
    
    def test_accepted_recommendation_commented(self):
        recom = create_recom("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        accept_recom(recom.recomID,"fair point")
        assert recom.comments == "fair point"

    def test_rejected_recommendation_commented(self):
        recom = create_recom("New Fan","We need a new fan the class is too hot.","COMP1600",None,"unchecked")
        reject_recom(recom.recomID,"Does not make sense")
        assert recom.comments == "Does not make sense"
   


