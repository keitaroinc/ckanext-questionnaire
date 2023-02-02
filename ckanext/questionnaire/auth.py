import ckan.plugins.toolkit as toolkit


def answer_create(context, data_dict):
    userobj = context.get('auth_user_obj')
    if not userobj:
        raise toolkit.NotAuthorized
    return {'success': True}


def question_edit(context, data_dict):
    return {'success': False}


def question_create(context, data_dict):
    return {'success': False}


def question_list(context, data_dict):
    return {'success': False}