import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate, db
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users )

import csv
from App.models import User, Staff, Student


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    with open('/workspace/Asg1-/App/students.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
    
        for row in reader:
            print(row)
            student = Student(studID=row['\ufeffstudID'],email=row['studEmail'],password=row['studPassword'],courseR1=row['courseR1'],courseR2=row['courseR2'],courseR3=row['courseR3'],courseR4=row['courseR4'],courseR5=row['courseR5'])
            #print(student.toJSON())
            db.session.add(student)
            db.session.commit()

    print('database intialized1')

    with open('/workspace/Asg1-/App/staff.csv', newline='') as csvfile:
        reader1 = csv.DictReader(csvfile)
    
        for row in reader1:
            print(row)
            staff = Staff(staffID=row['\ufeffstaffID'],email=row['staffEmail'],password=row['staffPassword'],course1=row['course1'],course2=row['course2'],course3=row['course3'])
            #print(student.toJSON())
            db.session.add(staff)
            db.session.commit()

    print('database intialized2')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Generic Commands
'''

#@app.cli.command("init")
#def initialize():
#    create_db(app)
#    print('database intialized')

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)