import os
from flask import Flask, request
from datetime import datetime
import jwt
import importlib.util
import random
import argon2
from functools import wraps

spec = importlib.util.spec_from_file_location("security", "tools/security.py")
suc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suc)

spec = importlib.util.spec_from_file_location("insert", "tools/insert.py")
insert = importlib.util.module_from_spec(spec)
spec.loader.exec_module(insert)

spec = importlib.util.spec_from_file_location("edit", "pdf_editor/edit.py")
edit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edit)

spec = importlib.util.spec_from_file_location("fiels", "tools/files.py")
files = importlib.util.module_from_spec(spec)
spec.loader.exec_module(files)

spec = importlib.util.spec_from_file_location("connector", "DataBase/connector.py")
connector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(connector)


# debuge mode
debug = True

# create the Flask app
app = Flask(__name__)

# set the secret key
app.config['SECRET_KEY'] = 'your-secret-key'

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator():
        token = None
        # ensure the jwt-token is passed with the headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token: # throw error if no token provided
            return "{'message': 'A valid token is missing!'}"
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if data['public_id'] == None:
                raise Exception()
            
        except:
            return "{'message': 'Invalid token!'}"
         # Return the user information attached to the token
        return f(data['public_id'])
    return decorator

# Login method responsible for generating authentication tokens
@app.route('/login', methods=['POST'])
def login():
    '''
        this function is used to login the user and generate a token for him
        the function returns a json object with the token
    '''

    # check if the request has the dict part
    try:
        auth = request.form.to_dict()
    except:
        return "{'message': 'there is no json object in the request'}"

    # check if the request has the username and password
    if 'username' not in auth or 'password' not in auth:
        return "{'message': 'there is no username or password'}"
    
    # check if the username and password are correct
    password = bytes(auth['password'], 'UTF-8')
    # get the users passaword hash from database 
    users = connector.run_sql("SELECT password_hash, id FROM Users WHERE username = '" + auth['username'] + "'")
    if len(users) == 0:
        return "{'message': 'username does not exist'}"
    
    password_hash = bytes(users[0][0][2: -1], 'UTF-8')
    public_id = users[0][1]

    # check if the password is correct
    try:
        argon2.verify_password(password_hash, password)  
    except:
        return "{'message': 'username or password is wrong'}"


    # generate the token
    token = jwt.encode({'public_id':  public_id}, app.config['SECRET_KEY'], 'HS256')

    return  "{'token': " + str(token) + "}"

@app.route('/questions', methods=['GET'])
def get_subjects():
    return "{'questions':"+ str(files.give_question_subjects()) +"}"

@app.route('/questions/<subject>', methods=['GET'])
def get_hardness(subject):
    return "{'hardness':"+ str(files.give_question_hardness(subject)) +"}"

@app.route('/team/<team_id>', methods=['GET'])
def get_team_name(team_id):
    return "{'name':'"+ str(list(connector.run_sql("SELECT name FROM Teams WHERE id = " + team_id))[0][0]) +"'}"

@app.route('/get_question', methods=['POST'])
@token_required
def get_question(user_id):
    # team_number subject hardness
    info = request.form.to_dict()
    
    # check if all the data for the request exist
    if 'team_number' not in info or 'subject' not in info or 'hardness' not in info:
        return "{'error':'missing data'}"
    
    questions_that_already_get =[i[0] for i in connector.run_sql("SELECT question_number FROM Problems WHERE team_id = " + info['team_number'])]
    questions_of_subject_and_hardness = files.get_question_numbers(info['subject'], info['hardness'])
    list_of_questions = [i for i in questions_of_subject_and_hardness if i[:-4] not in questions_that_already_get]

    # check if there is any question left
    if len(list_of_questions) == 0:
        return "{'error':'no question left'}"

    # choose a random question
    question_number = random.choice(list_of_questions)

    # generae the pdf file
    price, total_score = files.get_price_total_score(info['subject'], info['hardness'])
    location = 'questions/' + info['subject'] + '/' + info['hardness']+'-'+str(price)+'-'+str(total_score) + '/' + question_number

    pdf_info = {"headers":{
                    "team_number": info['team_number'],
                    "team_name": str(list(connector.run_sql("SELECT name FROM Teams WHERE id = " + info['team_number']))[0][0]),
                    "date": datetime.now().strftime("%H:%M"),
                    "price": str(price),
                    "question_number": str(question_number[:-4]),
                    "subject": info['subject'],
                    "hardness": info['hardness'],
                    "score": str(total_score)
                    },
                    "questions": [[str(i[0]), str(i[1]*i[2]//100)] for i in connector.run_sql("SELECT question_number, score, total_score FROM Problems WHERE team_id = " + info['team_number'])],
                    "subjects": [],
                }
    edit.edit(location, pdf_info)

    # add the question to the teams table
    cell = connector.run_sql("SELECT stage1_problems FROM Teams WHERE id = " + info['team_number'])[0][0]
    connector.run_sql("UPDATE Teams SET `stage1_problems` = '" + cell+" "+question_number[:-4] +"' WHERE (`id` = '" + info['team_number'] +"');")

    # add the question to the problems table
    insert.insert_problem(question_number[:-4], info['subject'], info['hardness'], info['team_number'], str(user_id), datetime.now().strftime("%H:%M"), price, total_score)

    return "{'message': 'Done!'}"

app.route('/give_question', methods=['POST'])
@token_required
def give_question(user_id):
    pass


if __name__ == '__main__':
    app.run(debug=debug, port=12345)

