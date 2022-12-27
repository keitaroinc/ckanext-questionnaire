import datetime

import ckan.plugins.toolkit as toolkit

import ckanext.questionnaire.helpers as ckanext_helpers

from ckanext.questionnaire.model import Question, QuestionOption, Answer


ValidationError = toolkit.ValidationError
asbool = toolkit.asbool


def question_create(context, data):

    session = context.get('session')
    question = Question()

    if not data.get('question-text'):
        raise ValidationError('Missing value')

    question.question_text = data.get("question-text")
    question.question_type = data.get("question-type")
    question.mandatory = data.get('question-required')

    session.add(question)
    if not data.get('question-option'):
        session.commit()

    for option in data.get('question-option'):
        question_option = QuestionOption()
        question_option.question_id = question.id
        question_option.answer_text = option

        session.add(question_option)
        session.commit()
    return


def answer_create(context, data):

    session = context.get('session')
    model = context.get('model')
    userobj = context.get('auth_user_obj')

    data, errors = ckanext_helpers._validate(data)
    if errors:
        session.rollback()
        raise ValidationError('Missing value')

    for key, value in data.items():
        answer=Answer()
        answer.user_id = userobj.id
        answer.date_answered = str(datetime.datetime.now())
        answer.question_id = key
        answer.answer_text = value
        model.Session.add(answer)
        model.Session.commit()


def question_update(context, data_dict):

    model = context.get("model")
    session = context.get("session")
    for_update = False

    question_id = data_dict.get("id")
    question_text = data_dict.get("question-text")
    question_type = data_dict.get("question-type")

    question = model.Session.query(Question).get(question_id)
    if not question:
        raise toolkit.ObjectNotFound('Question Not Found')

    if question_text and question_text not in question.question_text:
        question.question_text = question_text
        for_update = True

    if question_type and asbool(question_type) != question.mandatory:
        question.mandatory = asbool(question_type)
        for_update = True

    if for_update:
        session.add(question)
        session.commit()
    return
