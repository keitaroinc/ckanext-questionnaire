import sys
import click
import ckanext.questionnaire.utils as utils


def get_commands():
    return [questionnaire]

@click.group()
def questionnaire():
        """
    Questionnaire analysis of CKAN resources

    """

@questionnaire.command()
def init_db():
     utils.init_db()


@questionnaire.command()
def dell_db():
     utils.drop_db()