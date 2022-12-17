import sys
from sqlalchemy import or_
import logging
log = logging.getLogger(__name__)


def init_db():
    import ckan.model as model
    from ckanext.questionnaire.model import init_tables
    init_tables(model.meta.engine)


def drop_db():
    import ckan.model as model
    from ckanext.questionnaire.model import del_all_tables
    del_all_tables(model.meta.engine)