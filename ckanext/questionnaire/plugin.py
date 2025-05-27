import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

# from ckan.views.user import _get_repoze_handler
import ckanext.questionnaire.cli as cli
import ckanext.questionnaire.actions as actions
import ckanext.questionnaire.auth as auth
from ckanext.questionnaire.views import questionnaire, custom_login


class QuestionnairePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IAuthenticator, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)

    # IAuthenticator
    def login(self):
        return custom_login()


    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('assets', 'questionnaire')

    # IAction

    def get_actions(self):
        return {
            "question_create": actions.question_create,
            "answer_create": actions.answer_create,
            "question_update": actions.question_update,
            "answered_question": actions.answered_question,
            "answered_question_update": actions.answered_question_update
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            "answer_create": auth.answer_create,
            "question_create": auth.question_create,
            "question_edit": auth.question_edit,
            "question_list": auth.question_list
        }

    # ITemplateHelpers

    def get_helpers(self):
        return {}

    # IBlueprint

    def get_blueprint(self):
        return questionnaire

    # IClick

    def get_commands(self):
        return cli.get_commands()
