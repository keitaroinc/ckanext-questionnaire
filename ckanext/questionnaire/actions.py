import ckan.plugins.toolkit as toolkit

from ckanext.questionnaire.model import Question, QuestionOption


ValidationError = toolkit.ValidationError


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