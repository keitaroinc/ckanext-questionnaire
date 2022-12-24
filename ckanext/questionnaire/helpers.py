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
    for idx, question in enumerate(q_list):
        for answ in answered:
            if question.id == answ.question_id:
                del q_list[idx]
    return q_list


def _validate(data):

    for key, value in data.items():
        question = model.Session.query(Question).get(key)
        if question.mandatory and not value:
            return data, {'Missing value': question.question_text}

    return data, {}