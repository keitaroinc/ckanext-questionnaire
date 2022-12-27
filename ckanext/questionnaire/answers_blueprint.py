import ckan.lib.helpers as h
import flask, requests, os
import pandas as pd
import csv
import ckan.model as model
from flask import send_file, Response, Blueprint
from ckan.common import g
from ckanext.questionnaire.model import  Answer, Question
import ckan.plugins.toolkit as toolkit
from pathlib import Path
from flask import after_this_request


def download_answers():
    user_obj = g.userobj
    if user_obj and user_obj.sysadmin:
        y=str(Path().absolute())
        answer_db = model.Session.query(Answer).all()
        def answer_to_tuple(answer):
            return (answer.user, answer.question_text, answer.answer_text, answer.date_answered)
        
        with open("answers.csv", "w") as stream:
            writer = csv.writer(stream)
            writer.writerow(["User", "Question", "Answer ", "Date answered"])
            for answ in answer_db:
                row = answer_to_tuple(answ)
                writer.writerow(row)
        
        @after_this_request        
        def remove_file(response):
            os.remove('answers.csv')
            return response

    else:
        return Response("Page Not Found", status=400,)

    return send_file( y + '/answers.csv', mimetype='text/csv' , as_attachment=True)


###################################
# Combined user profile + answers #
###################################
def download_user_answers():

    y=str(Path().absolute())
    users_list = toolkit.get_action('user_list')({},{})
    df = pd.DataFrame()

    q_list = model.Session.query(Question).all()
    columns=['username', 'fullname', 'email']
    for col in q_list:
        #columns.append(col.id)
        columns.append(col.question_text)

    df = pd.concat([df, pd.DataFrame([columns])])
    
  
    for r in users_list:
        
        user_answers=model.Session.query(Answer).filter(Answer.user == (r['name'])).all()
        for answer in user_answers:
            pass
        insert_row = (r['name'], r['fullname'], r['email'])
        df = pd.concat([df, pd.DataFrame([insert_row])])
    
    
    
    df.to_csv('profiles.csv', sep='\t')

    return send_file( y + '/profiles.csv', mimetype='text/csv' , as_attachment=True)

