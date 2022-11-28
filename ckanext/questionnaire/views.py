from flask import Blueprint, session, render_template
from flask.views import MethodView
from ckan.common import g
import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckanext.questionnaire.model import Question, Answer_option, Answer
from datetime import datetime
import sqlalchemy

questionnaire = Blueprint('questionnaire', __name__)


class CreateQuestionView(MethodView):

    def get(self):

        return toolkit.render("add_questions.html")

    def post(self):

        question = Question()
        question.question_text = toolkit.request.form.get("add-question")
        question.created = str(datetime.now())
        model.Session.add(question)
        model.Session.commit()
        session['question_id'] = question.id
        return toolkit.redirect_to(toolkit.url_for("questionnaire.add_answers"))


class AddAnswerView(MethodView):

    def get(self):

        return toolkit.render("add_answers.html")

    def post(self):

        answer_option=Answer_option()
        answer_option.question_id = session['question_id']
        answer_option.answer_text= toolkit.request.form.get("add-answer-option")
        model.Session.add(answer_option)
        model.Session.commit()

        return toolkit.redirect_to(toolkit.url_for("questionnaire.add_answers"))


class AnswersView(MethodView):

    def get(self):

        q_list = model.Session.query(Question).all()
        answer_list = model.Session.query(Answer_option).all()

        content={
            'q_list' : q_list,
            'answer_list' : answer_list
        }

        return render_template("answers.html", **content)

    def post(self):
        
        form_data = toolkit.request.form.to_dict()

        for x, y  in form_data.items():
            answer=Answer()
            answer.user_name = g.userobj.name
            answer.date_answered = str(datetime.now())
            answer.question_text = x
            answer.answer_text = y
            model.Session.add(answer)
            model.Session.commit()
                
        
        
        return toolkit.redirect_to(toolkit.url_for("questionnaire.answers"))



questionnaire.add_url_rule(
    '/add_questions', view_func=CreateQuestionView.as_view(str("add_questions")))
questionnaire.add_url_rule(
    '/add_answers', view_func=AddAnswerView.as_view(str("add_answers")))
questionnaire.add_url_rule(
    '/answers', view_func=AnswersView.as_view(str("answers")))
