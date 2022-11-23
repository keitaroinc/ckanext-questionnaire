import ckan.plugins.toolkit as toolkit

def add_questions():
    u'''A simple view function'''
    return toolkit.render("add_questions.html")

def answers():
    u'''A simple view function'''
    return toolkit.render("answers.html")