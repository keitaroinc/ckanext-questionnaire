from flask import Blueprint
from flask.views import MethodView

import ckan.model as model
import ckan.logic as logic
import ckan.plugins.toolkit as toolkit
import ckan.lib.navl.dictization_functions as dict_fns

from ckan.common import _, g, request,  current_user, login_user

import ckanext.questionnaire.helpers as ckanext_helpers

from ckanext.questionnaire.model import Question, QuestionOption, Answer
from ckanext.questionnaire.answers_blueprint import download_answers

import ckan.lib.authenticator as authenticator
import ckan.lib.base as base
from ckan.views.user import next_page_or_default, rotate_token
from ckan.lib.helpers import helper_functions as h

clean_dict = logic.clean_dict
tuplize_dict = logic.tuplize_dict
parse_params = logic.parse_params
ValidationError = toolkit.ValidationError
NotFound = toolkit.ObjectNotFound
NotAuthorized = toolkit.NotAuthorized

questionnaire = Blueprint("questionnaire", __name__)

not_found_message = (
    "The requested URL was not found on the server. "
    "If you entered the URL manually please check your spelling and try again."
)


class CreateQuestionView(MethodView):
    def _prepare(self):
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }
        try:
            toolkit.check_access("question_create", context)
        except:
            return toolkit.abort(404, toolkit._(not_found_message))
        return context

    def get(self, errors=None):
        self._prepare()

        qtype = ckanext_helpers.get_question_type()
        qrequire = ckanext_helpers.get_question_require()
        qtext = ckanext_helpers.get_question_text()
        qoption = ckanext_helpers.get_question_option()

        data = {}

        vars_option = dict(data=data, errors={}, **qoption)
        vars_type = dict(data=data, errors={}, **qtype)
        vars_qrequired = dict(data=data, errors={}, **qrequire)
        vars_qtext = dict(data=data, errors={}, **qtext)

        extra_vars = {
            "vars_type": vars_type,
            "vars_qrequired": vars_qrequired,
            "vars_qtext": vars_qtext,
            "vars_option": vars_option,
            "error": errors,
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
            return self.get([errors.get("message")])

        return toolkit.redirect_to(toolkit.url_for("questionnaire.question_list"))


class AnswersView(MethodView):
    def _prepare(self):
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }
        try:
            toolkit.check_access("answer_create", context)
        except:
            return toolkit.abort(404, toolkit._(not_found_message))
        return context

    def get(self, errors={}):
        context = self._prepare()
        session = context.get("session")

        q_list = session.query(Question).all()
        q_option_list = session.query(QuestionOption).all()
        q_list = ckanext_helpers.check_and_delete_answered(q_list)

        extra_vars = {"q_list": q_list, "q_option_list": q_option_list, "error": errors}
        return toolkit.render("answers.html", extra_vars)

    def post(self):

        context = self._prepare()
        form_data = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(toolkit.request.form)))
        )

        try:
            toolkit.get_action("answer_create")(context, form_data)
        except ValidationError as e:
            errors = e.error_dict
            return self.get([errors.get("message")])

        return toolkit.redirect_to("questionnaire.answered")


class EditQuestionView(MethodView):
    def _prepare(self):
        context = {
            "model": model,
            "session": model.Session,
            "user": g.user,
            "auth_user_obj": g.userobj,
        }
        try:
            toolkit.check_access("question_edit", context)
        except:
            return toolkit.abort(404, toolkit._(not_found_message))
        return context

    def get(self, question_id):
        self._prepare()

        question = model.Session.query(Question).get(question_id)
        q_options = QuestionOption.get(question_id)
        qrequire = ckanext_helpers.get_question_require()
        extra_vars = {
            "question": question,
            "qrequire": qrequire,
            "q_options": q_options,
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

    extra_vars: dict[str, Any] = {}

    if current_user.is_authenticated:
        return base.render("user/logout_first.html", extra_vars)

    if request.method == "POST":
        username_or_email = request.form.get("login")
        password = request.form.get("password")
        _remember = request.form.get("remember")

        identity = {
            u"login": username_or_email,
            u"password": password
        }

        user_obj = authenticator.ckan_authenticator(identity)

        if user_obj:
            answered = Answer.get(user_obj.id)
            if user_obj.sysadmin or not ckanext_helpers.has_unanswered_questions(answered):
                next = request.args.get('next', request.args.get('came_from'))
            else:
                next = "/answers"
            if _remember:
                from datetime import timedelta
                duration_time = timedelta(milliseconds=int(_remember))
                login_user(user_obj, remember=True, duration=duration_time)
                rotate_token()
                return next_page_or_default(next)
            else:
                login_user(user_obj)
                rotate_token()
                return next_page_or_default(next)
        else:
            err = _(u"Login failed. Bad username or password.")
            h.flash_error(err)
            return base.render("user/login.html", extra_vars)

    return base.render("user/login.html", extra_vars)


def question_list():
    context = {
        "model": model,
        "session": model.Session,
        "user": g.user,
        "auth_user_obj": g.userobj,
    }

    try:
        toolkit.check_access("question_list", context)
    except:
        return toolkit.abort(404, toolkit._(not_found_message))

    q_list = model.Session.query(Question).all()
    extra_vars = {"q_list": q_list}
    return toolkit.render("question_read.html", extra_vars)


def answered():
    context = {
        "model": model,
        "session": model.Session,
        "user": g.user,
        "auth_user_obj": g.userobj,
    }

    try:
        answered = toolkit.get_action("answered_question")(context, {})
    except:
        toolkit.abort(404, toolkit._("User not found"))

    extra_vars = {"answered": answered}
    return toolkit.render("answered_question.html", extra_vars)


def answered_edit(answered_id):
    context = {
        "model": model,
        "session": model.Session,
        "user": g.user,
        "auth_user_obj": g.userobj,
    }
    data_dict = {"answered_id": answered_id}

    try:
        answered = toolkit.get_action("answered_question")(context, data_dict)
    except (NotFound, NotAuthorized):
        toolkit.abort(404, toolkit._("Question not found"))

    for answ in answered:
        if answ.get("id") == answered_id:
            break

    if request.method == "POST":
        form_data = clean_dict(
            dict_fns.unflatten(tuplize_dict(parse_params(toolkit.request.form)))
        )
        updated_answer = form_data.get("answered-text") or form_data.get(
            "question-type"
        )
        if updated_answer != answ.get("answer_text"):
            data_dict.update({"updated_answer": updated_answer})

            toolkit.get_action("answered_question_update")(context, data_dict)
            return toolkit.redirect_to("questionnaire.answered")

    question_opts = QuestionOption.get(answ.get("question_id"))
    q_opts = [
        {"key": q_opts.answer_text, "value": q_opts.answer_text}
        for q_opts in question_opts
    ]
    extra_vars = {"answered": answ, "q_opts": q_opts}
    return toolkit.render("answered_edit.html", extra_vars)


def delete(question_id):

    if toolkit.request.method == "POST":
        model.Session.query(QuestionOption).filter(
            QuestionOption.question_id == question_id
        ).delete()
        model.Session.query(Answer).filter(Answer.question_id == question_id).delete()
        model.Session.commit()
        model.Session.query(Question).filter(Question.id == question_id).delete()
        model.Session.commit()
        return toolkit.redirect_to("questionnaire.question_list")

    return toolkit.render(
        "question_delete.html", extra_vars={"question_id": question_id}
    )


questionnaire.add_url_rule(
    "/add_questions", view_func=CreateQuestionView.as_view(str("add_questions"))
)
questionnaire.add_url_rule(
    "/questions", view_func=question_list, methods=("GET", "POST")
)
questionnaire.add_url_rule(
    "/<question_id>/delete", view_func=delete, methods=("GET", "POST")
)
questionnaire.add_url_rule("/answers", view_func=AnswersView.as_view(str("answers")))
questionnaire.add_url_rule("/answered", view_func=answered)
questionnaire.add_url_rule(
    "/answered/<answered_id>/edit", view_func=answered_edit, methods=("GET", "POST")
)
questionnaire.add_url_rule(
    "/<question_id>/edit", view_func=EditQuestionView.as_view(str("edit"))
)
questionnaire.add_url_rule("/download_answers", view_func=download_answers)
