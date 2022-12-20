from flask import Blueprint, session, render_template
from flask.views import MethodView
from ckan.common import g
import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckanext.questionnaire.model import Question, QuestionOption, Answer
from ckanext.questionnaire.answers_blueprint import download_answers
from ckanext.questionnaire.helpers import preprare_list, q_text, questions_select_one
from datetime import datetime


questionnaire = Blueprint('questionnaire', __name__)




def get_question():
    types = [{'text': 'Text',
            'value': 'text' },
            {'text': 'Select One',
            'value': 'select_one' },
            {'text': 'Select One',
            'value': 'select_many' },
            ]
    name='Question type'

    return dict(types=types, name=name)


class CreateQuestionView(MethodView):
    
    

    def get(self):
        items = get_question()
        data={}
        vars = dict(data=data, errors={}, **items)

        return render_template("add_questions.html", extra_vars=vars )

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
        
        return toolkit.redirect_to(toolkit.url_for("questionnaire.add_question_option"))

# AddAnswerView Not in use now
class AddQuestionOption(MethodView):

    def get(self):

        return toolkit.render("add_question_options.html")

    def post(self):

        question_option=QuestionOption()
        question_option.question_id = session['question_id']
        question_option.answer_text= toolkit.request.form.get("add_question_option")
        model.Session.add(question_option)
        model.Session.commit()

        return toolkit.redirect_to(toolkit.url_for("questionnaire.add_question_option"))



class AnswersView(MethodView):



    def get(self):

        items = get_question()
        q_list = model.Session.query(Question).all()
        q_option_list = model.Session.query(QuestionOption).all()
        select_list = questions_select_one(*q_list, *q_option_list)
        data={}
        vars = dict(data=data, errors={}, **items)
        content={
            'q_list' : q_list,
            'q_option_list' : q_option_list,
            'select_list' : select_list,
        }

        return render_template("answers.html", extra_vars=vars)

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

