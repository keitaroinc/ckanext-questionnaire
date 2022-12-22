from flask import Blueprint, session, render_template, request, jsonify
from flask.views import MethodView
from ckan.common import g
import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckanext.questionnaire.model import Question, QuestionOption, Answer
from ckanext.questionnaire.answers_blueprint import download_answers
from ckanext.questionnaire.helpers import *
from datetime import datetime


questionnaire = Blueprint('questionnaire', __name__)


class CreateQuestionView(MethodView):
    

    def get(self):
        
        qtype = get_question_type()
        qrequire = get_question_require()
        qtext = get_question_text()
        data={}
        vars_type = dict(data=data, errors={}, **qtype)
        vars_qrequired= dict(data=data, errors={}, **qrequire)
        vars_qtext= dict(data=data, errors={}, **qtext)
        context={
            'vars_type' : vars_type,
            'vars_qrequired' : vars_qrequired,
            'vars_qtext' :vars_qtext
        }
        return render_template("add_questions.html", **context)

    def post(self):

        question = Question()
        
        question.question_text = toolkit.request.form.get("question-text")
        question.question_type = toolkit.request.form.get("question-type")
        question.mandatory=toolkit.request.form.get('question-required')
        question.created = str(datetime.now())
        model.Session.add(question)
        model.Session.commit()
   
        session['question_id'] = question.id
      
        
        return toolkit.redirect_to(toolkit.url_for("questionnaire.add_question_option"))

# AddAnswerView Not in use now
class AddQuestionOption(MethodView):

    def get(self):

        qoption = get_question_option()
        data={}
        vars_option = dict(data=data, errors={}, **qoption)

        return render_template("add_question_options.html", vars_option=vars_option)

    def post(self):

        question_option=QuestionOption()
        question_option.question_id = session['question_id']
        question_option.answer_text= toolkit.request.form.get("question-option")
        model.Session.add(question_option)
        model.Session.commit()

        return toolkit.redirect_to(toolkit.url_for("questionnaire.add_question_option"))



class AnswersView(MethodView):



    def get(self):

        q_list = model.Session.query(Question).all()
        q_option_list = model.Session.query(QuestionOption).all()
        context={
            'q_list' : q_list,
            'q_option_list' : q_option_list,
            }
         
        return render_template("answers.html", **context)

    def post(self):
        
        form_data = toolkit.request.form
        formdata = request.values

        if model.Session.query(Answer).filter( Answer.user_id == g.userobj.id).count() == 0 :

            # Save the answers to database
            for key, value in form_data.items(multi=True):
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



questionnaire.add_url_rule(
    '/add_questions', view_func=CreateQuestionView.as_view(str("add_questions")))
questionnaire.add_url_rule(
    '/add_question_option', view_func=AddQuestionOption.as_view(str("add_question_option")))
questionnaire.add_url_rule(
    '/answers', view_func=AnswersView.as_view(str("answers")))
questionnaire.add_url_rule(
    '/download_answers', view_func=download_answers)
questionnaire.add_url_rule(
    '/delete_questions/', view_func=DeleteQuestionView.as_view(str("delete_questions")))

