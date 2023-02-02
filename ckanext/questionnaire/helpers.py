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
    if not answered:
        return q_list

    new_list = []

    for question in q_list:
        if question.id in [answ.question_id for answ in answered]:
            continue
        else:
            new_list.append(question)

    return new_list


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


def is_valid_uuid(value):
    import uuid

    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False
