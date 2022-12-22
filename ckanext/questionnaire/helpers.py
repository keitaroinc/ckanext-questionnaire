from ckanext.questionnaire.model import Question, QuestionOption
import ckan.model as model
from ckan.lib import base
import sqlalchemy as db



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
