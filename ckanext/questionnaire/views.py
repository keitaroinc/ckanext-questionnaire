from flask import Blueprint
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

    def _prepare(self):
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'auth_user_obj': g.userobj,
        }
        try:
            toolkit.check_access(u'question_create', context)
        except:
            return toolkit.abort(404, toolkit._(not_found_message))
        return context

    def get(self, errors=None):
        self._prepare()

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
        return toolkit.render("add_questions.html", extra_vars)

    def post(self):

        context = self._prepare()
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

    def _prepare(self):
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'auth_user_obj': g.userobj,
        }
        try:
            toolkit.check_access(u'answer_create', context)
        except:
            return toolkit.abort(404, toolkit._(not_found_message))
        return context

    def get(self, errors={}):
        self._prepare()

        q_list = model.Session.query(Question).all()
        q_option_list = model.Session.query(QuestionOption).all()
        q_list = ckanext_helpers.check_and_delete_answered(q_list)

        extra_vars = {
            'q_list' : q_list,
            'q_option_list' : q_option_list,
            'error': errors
        }
        return toolkit.render("answers.html", extra_vars)

    def post(self):

        context = self._prepare()
        form_data = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(toolkit.request.form)))
        )

        try:
            toolkit.get_action('answer_create')(context, form_data)
        except ValidationError as e:
            errors = e.error_dict
            return self.get([errors.get('message')])

        return toolkit.redirect_to(toolkit.url_for("dashboard.index"))


class EditQuestionView(MethodView):

    def _prepare(self):
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'auth_user_obj': g.userobj,
        }
        try:
            toolkit.check_access(u'question_edit', context)
        except:
            return toolkit.abort(404, toolkit._(not_found_message))
        return context

    def get(self, question_id):
        self._prepare()

        question = model.Session.query(Question).get(question_id)
        qrequire = ckanext_helpers.get_question_require()
        extra_vars = {
            "question": question,
            "qrequire": qrequire
        }

        return toolkit.render("question_edit.html", extra_vars)

    def post(self, question_id):

        context = self._prepare()
        data_dict = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(toolkit.request.form)))
        )
        data_dict.update({"id": question_id})

        try:
            toolkit.get_action("question_update")(context, data_dict)
        except:
            # TODO
            pass

        return toolkit.redirect_to("questionnaire.question_list")


def custom_login():

    route_after_login = toolkit.config.get('ckan.route_after_login')
    if g.user and g.userobj.sysadmin:
        return toolkit.redirect_to(route_after_login)

    if g.user and g.userobj:
        answered = Answer.get(g.userobj.id)
        if not answered or ckanext_helpers.has_unanswered_questions(answered):
            return toolkit.redirect_to("questionnaire.answers")

        # if has_unanswered_questions(answered):
        #     return toolkit.redirect_to("questionnaire.answers")

        return toolkit.redirect_to(route_after_login)

    err = toolkit._(u'Login failed. Bad username or password.')
    toolkit.h.flash_error(err)
    return toolkit.redirect_to('user.login')


def question_list():
    context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'auth_user_obj': g.userobj,
        }

    try:
        toolkit.check_access(u'question_edit', context)
    except:
        return toolkit.abort(404, toolkit._(not_found_message))

    q_list = model.Session.query(Question).all()
    extra_vars = {"q_list" : q_list}
    return toolkit.render("question_read.html", extra_vars)


def delete(question_id):

    if toolkit.request.method == "POST":
        model.Session.query(QuestionOption).filter(QuestionOption.question_id == question_id).delete()
        model.Session.query(Answer).filter(Answer.question_id == question_id).delete()
        model.Session.commit()
        model.Session.query(Question).filter(Question.id == question_id).delete()
        model.Session.commit()
        return toolkit.redirect_to("questionnaire.question_list")

    return toolkit.render("question_delete.html", extra_vars={"question_id": question_id})


questionnaire.add_url_rule(
    '/add_questions', view_func=CreateQuestionView.as_view(str("add_questions")))
questionnaire.add_url_rule('/login', view_func=custom_login, methods=('GET', 'POST'))
questionnaire.add_url_rule('/questions', view_func=question_list, methods=('GET', 'POST'))
questionnaire.add_url_rule('/<question_id>/delete', view_func=delete, methods=('GET', 'POST'))
questionnaire.add_url_rule(
    '/answers', view_func=AnswersView.as_view(str("answers")))
questionnaire.add_url_rule(
    '/<question_id>/edit', view_func=EditQuestionView.as_view(str("edit")))
questionnaire.add_url_rule(
    '/download_answers', view_func=download_answers)
