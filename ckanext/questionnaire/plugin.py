import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.views.user import _get_repoze_handler

import ckanext.questionnaire.cli as cli
import ckanext.questionnaire.actions as actions
import ckanext.questionnaire.auth as auth

from ckanext.questionnaire.views import questionnaire


class QuestionnairePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IAuthenticator, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)

    # IAuthenticator

    def identify(self):
        response = None
        return response

    def login(self):

        extra_vars = {}
        if toolkit.g.user:
            return toolkit.base.render(u'user/logout_first.html', extra_vars)

        came_from = toolkit.request.params.get(u'came_from')
        if not came_from:
            came_from = toolkit.url_for('questionnaire.custom_login')
        toolkit.g.login_handler = toolkit.url_for(_get_repoze_handler(u'login_handler_path'), came_from=came_from)

        return toolkit.base.render(u'user/login.html', extra_vars)

    def logout(self):
        response = None
        return response

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
