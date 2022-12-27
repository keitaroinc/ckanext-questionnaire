import ckan.model as model

from ckan.common import g

from ckanext.questionnaire.model import Answer, Question


def get_question_type():
    types = [{'text': 'Text',
            'value': 'text' },
            {'text': 'Select One',
            'value': 'select_one' },
            {'text': 'Select Many',
            'value': 'select_many' },
            ]
    name='question-type'
    label='Question type'
    id='field-question-type'

    return dict(types=types, name=name, label=label, id=id)


def get_question_require():
    types = [{'text': 'Yes',
            'value': True },
            {'text': 'No',
            'value': False },
            ]
    name='question-requred'
    label='Question required'
    id='field-question-required'

    return dict(types=types, name=name, label=label, id=id)


def get_question_text():

    name='question-text'
    label='Question text'
    id='field-question-text'

    return dict(name=name, label=label, id=id)


def get_question_option():

    name='question-option'
    label='Question option'
    id='field-question-option'

    return dict(name=name, label=label, id=id)


def check_and_delete_answered(q_list):
    answered = Answer.get(g.userobj.id)
    sorted_answ = sorted(answered, key=lambda answ: answ.question_id, reverse=True)
    sorted_q_list = sorted(q_list, key=lambda question: question.id, reverse=True)
    q_list = []

    for question, answers in zip(sorted_q_list, sorted_answ):
        if question.id == answers.question_id:
            continue
        else:
            q_list.append(question)

    return q_list


def _validate(data):

    for key, value in data.items():
        question = model.Session.query(Question).get(key)
        if question.mandatory and not value:
            return data, 'Missing value'

    return data, {}


def has_unanswered_questions(answered):
    all_questions = model.Session.query(Question).all()
    if len(all_questions) > len(answered):
        return True
    return False
