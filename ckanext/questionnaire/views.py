from datetime import datetime

from flask import Blueprint, render_template, request
from flask.views import MethodView

import ckan.model as model
import ckan.logic as logic
import ckan.plugins.toolkit as toolkit
import ckan.lib.navl.dictization_functions as dict_fns

from ckan.common import g

import ckanext.questionnaire.helpers as ckanext_helpers

from ckanext.questionnaire.model import Question, QuestionOption, Answer
from ckanext.questionnaire.answers_blueprint import download_answers


clean_dict = logic.clean_dict
tuplize_dict = logic.tuplize_dict
parse_params = logic.parse_params
ValidationError = toolkit.ValidationError

questionnaire = Blueprint('questionnaire', __name__)

not_found_message = (
    'The requested URL was not found on the server. '
    'If you entered the URL manually please check your spelling and try again.'
)


class CreateQuestionView(MethodView):

    def get(self, errors=None):

        if not g.user or g.user and not g.userobj.sysadmin:
            return toolkit.abort(404, toolkit._(not_found_message))

        qtype = ckanext_helpers.get_question_type()
        qrequire = ckanext_helpers.get_question_require()
        qtext = ckanext_helpers.get_question_text()
        qoption = ckanext_helpers.get_question_option()

        data={}

        vars_option = dict(data=data, errors={}, **qoption)
        vars_type = dict(data=data, errors={}, **qtype)
        vars_qrequired= dict(data=data, errors={}, **qrequire)
        vars_qtext= dict(data=data, errors={}, **qtext)

        extra_vars = { 
            'vars_type': vars_type,
            'vars_qrequired': vars_qrequired,
            'vars_qtext': vars_qtext,
            'vars_option': vars_option,
            'error': errors
        }
        return toolkit.base.render("add_questions.html", extra_vars)

    def post(self):

        context = {}
        data = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(toolkit.request.form)))
        )

        try:
            toolkit.get_action("question_create")(context, data)
        except ValidationError as e:
            errors = e.error_dict
            return self.get([errors.get('message')])

        return toolkit.redirect_to(toolkit.url_for("dashboard.datasets"))


class AnswersView(MethodView):

    def get(self, data=None, errors={}):

        if not g.user:
            return toolkit.abort(404, toolkit._(not_found_message))

        q_list = model.Session.query(Question).all()
        q_option_list = model.Session.query(QuestionOption).all()
        q_list = ckanext_helpers.check_and_delete_answered(q_list)
        context = {
            'data': data,
            'q_list' : q_list,
            'q_option_list' : q_option_list,
            'error': errors
        }

        return render_template("answers.html", **context)

    def post(self):

        form_data = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(toolkit.request.form)))
        )

        data, errors = ckanext_helpers._validate(form_data)
        if errors:
            return self.get(form_data, errors)
            # model.Session.rollback()
            # raise ValidationError(errors)

        if model.Session.query(Answer).filter( Answer.user_id == g.userobj.id).count() == 0 :

            # Save the answers to database
            for key, value in data.items():
                answer=Answer()
                answer.user_id = g.userobj.id
                answer.date_answered = str(datetime.now())
                answer.question_id = key
                answer.answer_text = value
                model.Session.add(answer)
                model.Session.commit()
    
        else:
            #delete previous answers
            model.Session.query(Answer).filter(Answer.user_id == g.userobj.id).delete()
            model.Session.commit()
            
            # Save the answers to database
            for key, value in form_data.items(multi=True):
                answer=Answer()
                answer.user_id = g.userobj.name
                answer.date_answered = str(datetime.now())
                answer.question_id = key
                answer.answer_text = value
                model.Session.add(answer)
                model.Session.commit()

        
        return toolkit.redirect_to(toolkit.url_for("dashboard.index"))

class DeleteQuestionView(MethodView):

    def get(self):
        q_list = model.Session.query(Question).all()

        context={
            'q_list' : q_list
        }
        return render_template("delete_questions.html", **context)

    def post(self):
        
        qid=toolkit.request.form.get('qid')
        try:
            model.Session.query(QuestionOption).filter(QuestionOption.question_id == qid).delete()
            model.Session.commit()
            model.Session.query(Question).filter(Question.id == qid).delete()
            model.Session.commit()
        except Exception as e:
            pass

        return toolkit.redirect_to(toolkit.url_for("questionnaire.delete_questions"))


def has_unanswered_questions(answered):
    all_questions = model.Session.query(Question).all()
    if len(all_questions) > len(answered):
        return True
    return False


def custom_login():

    route_after_login = toolkit.config.get('ckan.route_after_login')
    if g.user and g.userobj.sysadmin:
        return toolkit.redirect_to(route_after_login)

    if g.user and g.userobj:
        answered = Answer.get(g.userobj.id)
        if not answered:
            return toolkit.redirect_to("questionnaire.answers")

        if has_unanswered_questions(answered):
            return toolkit.redirect_to("questionnaire.answers")

        return toolkit.redirect_to(route_after_login)

    err = toolkit._(u'Login failed. Bad username or password.')
    toolkit.h.flash_error(err)
    return toolkit.redirect_to('user.login')


questionnaire.add_url_rule(
    '/add_questions', view_func=CreateQuestionView.as_view(str("add_questions")))
questionnaire.add_url_rule('/login', view_func=custom_login, methods=('GET', 'POST'))
questionnaire.add_url_rule(
    '/answers', view_func=AnswersView.as_view(str("answers")))
questionnaire.add_url_rule(
    '/download_answers', view_func=download_answers)
questionnaire.add_url_rule(
    '/delete_questions/', view_func=DeleteQuestionView.as_view(str("delete_questions")))
