from flask import Blueprint, session, render_template
from flask.views import MethodView
from ckan.common import g
import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckanext.questionnaire.model import Question, Answer_option, Answer
from ckanext.questionnaire.answers_blueprint import download_answers
from ckanext.questionnaire.func import preprare_list, q_text
from datetime import datetime
import sqlalchemy

questionnaire = Blueprint('questionnaire', __name__)


class CreateQuestionView(MethodView):

    def get(self):

        return toolkit.render("add_questions.html")

    def post(self):

        question = Question()
        
        question.question_text = toolkit.request.form.get("add-question")
        question.question_type = toolkit.request.form.get("question_type")
        mandatory=toolkit.request.form.get("mandatory")
        if mandatory=="Yes":
            question.mandatory = True
        else:
            question.mandatory = False
        question.created = str(datetime.now())
        model.Session.add(question)
        model.Session.commit()
        
        #answer_option=Answer_option()
        session['question_id'] = question.id
        #answer_option.question_id = session['question_id']
        #answer_option.answer_text= toolkit.request.form.get("add-answer-option")
        #model.Session.add(answer_option)
        #model.Session.commit()
        
        return toolkit.redirect_to(toolkit.url_for("questionnaire.add_questions"))

# AddAnswerView Not in use now
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
        #prepare data for checkpoint answers save
        final_data = preprare_list(**form_data)
        final_data = q_text(*final_data)

        if model.Session.query(Answer).filter( Answer.user_name == g.userobj.name).count() == 0 :

            # Save the answers to database
            for x in final_data:
                answer=Answer()
                answer.user_name = g.userobj.name
                answer.date_answered = str(datetime.now())
                answer.question_text = x[0]
                answer.answer_text = x[1]
                model.Session.add(answer)
                model.Session.commit()
                
        else:
            #delete previous answers
            model.Session.query(Answer).filter(Answer.user_name == g.userobj.name).delete()
            model.Session.commit()
            
            # Save the answers to database
            for x in final_data:
                answer=Answer()
                answer.user_name = g.userobj.name
                answer.date_answered = str(datetime.now())
                answer.question_text = x [0]
                answer.answer_text = x[1]
                model.Session.add(answer)
                model.Session.commit()

        
        return toolkit.redirect_to(toolkit.url_for("dashboard.index"))

class DeleteQuestionView(MethodView):

    def get(self):
        q_list = model.Session.query(Question).all()

        content={
            'q_list' : q_list
        }
        return render_template("delete_questions.html", **content)

    def post(self):
        
        qid=toolkit.request.form.get('qid')
        model.Session.query(Question).filter(Question.id == qid).delete()
        model.Session.commit()

            
        
        return toolkit.redirect_to(toolkit.url_for("questionnaire.delete_questions"))



questionnaire.add_url_rule(
    '/add_questions', view_func=CreateQuestionView.as_view(str("add_questions")))
questionnaire.add_url_rule(
    '/add_answers', view_func=AddAnswerView.as_view(str("add_answers")))
questionnaire.add_url_rule(
    '/answers', view_func=AnswersView.as_view(str("answers")))
questionnaire.add_url_rule(
    '/download_answers', view_func=download_answers)
questionnaire.add_url_rule(
    '/delete_questions/', view_func=DeleteQuestionView.as_view(str("delete_questions")))

