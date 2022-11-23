from flask import Blueprint

import ckan.plugins.toolkit as toolkit

questionnaire = Blueprint('questionnaire', __name__)


def add_questions():
    u'''A simple view function'''
    return toolkit.render("add_questions.html")

def answers():
    u'''A simple view function'''
    return toolkit.render("answers.html")

def add_answers():
    u'''A simple view function'''
    return toolkit.render("add_answers.html")

questionnaire.add_url_rule('/add_questions', view_func= add_questions)
questionnaire.add_url_rule('/answers', view_func= answers)
questionnaire.add_url_rule('/add_answers', view_func= add_answers)