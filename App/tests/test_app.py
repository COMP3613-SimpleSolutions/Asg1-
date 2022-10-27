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
        assert user.studID == "816026077"

    # pure function no side effects or integrations called
    def test_toJSON(self):
        student = Student(816026077,"bob.saget@studmail.com","bobpass","COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
        student_json = Student.toJSON()
        self.assertDictEqual(user_json, {"id":816026077, "course1" : "COMP1600","course2" : "COMP1601","course3" : "COMP1602","course4" : "COMP1603","course5" : "COMP1604",})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        student = Student(816026077,"bob.saget@studmail.com",password,"COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
        assert student.password != password

    def test_check_password(self):
        password = "mypass"
        student = Student(816026077,"bob.saget@studmail.com",password,"COMP1600","COMP1601","COMP1602","COMP1603","COMP1604")
        assert student.check_password(password)
