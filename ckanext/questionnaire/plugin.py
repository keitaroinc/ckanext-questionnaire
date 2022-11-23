from flask import Blueprint

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.questionnaire.views import questionnaire


class QuestionnairePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'questionnaire')

    def get_helpers(self):
        return {
        }

    def get_blueprint(self):
        return questionnaire
