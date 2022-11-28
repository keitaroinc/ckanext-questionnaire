import sys
import uuid
import datetime
from six import text_type

from sqlalchemy import Column, Unicode, types,  DateTime
from sqlalchemy.ext.declarative import declarative_base

import ckan.model as model
from ckan.lib import dictization
from ckan.plugins import toolkit

log = __import__('logging').getLogger(__name__)

Base = declarative_base()

def make_uuid():
    return text_type(uuid.uuid4())


if sys.version_info[0] >= 3:
    unicode = str


class Question(Base):

    __tablename__ = 'question'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    question_text = Column(types.UnicodeText, nullable=False, index=True)
    created = Column(types.DateTime, default=datetime.datetime.now)



class Answer_option(Base):
    
    __tablename__ = 'answer_option'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    question_id = Column(Unicode)
    answer_text = Column(types.UnicodeText, nullable=False, index=True)


class Answer(Base):

    __tablename__ = 'answer'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    question_text = Column(types.UnicodeText, nullable=False, index=True)
    user_name = Column(types.UnicodeText, nullable=False, index=True)
    answer_text = Column(types.UnicodeText, nullable=False, index=True)
    date_answered = Column(types.DateTime, default=datetime.datetime.now)


def create_tables():
    Question.__table__.create()
    Answer_option.__table__.create()
    Answer.__table__.create()

    log.info(u'Questionnarie database tables created')



def init_tables(engine):
    Base.metadata.create_all(engine)
    log.info('Questionnarie database tables created')

