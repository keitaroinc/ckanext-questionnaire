import ckan.lib.helpers as h
import flask, requests, os
import csv
import ckan.model as model
from flask import send_file, Response, Blueprint
from ckan.common import g
from ckanext.questionnaire.model import  Answer, Question
import ckan.plugins.toolkit as toolkit
from pathlib import Path
from flask import after_this_request
import ckan.logic as logic


def download_answers():
    user_obj = g.userobj
    if user_obj and user_obj.sysadmin:
        y=str(Path().absolute())
        answer_db = model.Session.query(Answer).all()

        def answer_to_tuple(user, question, answer):
            return (user['name'], user['fullname'], user['email'], question.question_text, answer.answer_text, answer.date_answered)
        
        with open("answers.csv", "w") as stream:
            writer = csv.writer(stream)
            writer.writerow(["Username", "User Fullname", "User email", "Question", "Answer ", "Date answered"])
            for answ in answer_db:
                question = model.Session.query(Question).get(answ.question_id)
                user = logic.get_action(u'user_show')({}, {'id': answ.user_id})

                row = answer_to_tuple(user, question, answ)
                writer.writerow(row)
        
        @after_this_request        
        def remove_file(response):
            os.remove('answers.csv')
            return response

    else:
        return Response("Page Not Found", status=400,)

    return send_file( y + '/answers.csv', mimetype='text/csv' , as_attachment=True)

