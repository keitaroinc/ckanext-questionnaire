import logging 
import datetime

from sqlalchemy import types, Table, Column, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import or_

import ckan.model as model

from ckan.common import g
from ckan.model.meta import metadata, mapper, Session
from ckan.model.domain_object import DomainObject
from ckan.model.types import make_uuid


log = logging.getLogger(__name__)

metadata = MetaData()


question_table = Table('question',metadata,
    Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
    Column('question_text', types.UnicodeText),
    Column('question_type', types.UnicodeText),
    Column('mandatory', types.Boolean, default=True),
    Column('created', types.DateTime, default=datetime.datetime.utcnow),
    )

question_option_table = Table('question_option',metadata,
    Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
    Column('question_id', ForeignKey('question.id')),
    Column('answer_text', types.UnicodeText, default=u'{}'),
    )

answer_table = Table('answer',metadata,
    Column('id', types.UnicodeText, primary_key=True, default=make_uuid),
    Column('question_id', ForeignKey('question.id')),
    Column('user_id', types.UnicodeText, default=u'{}'),
    Column('answer_text', types.UnicodeText, default=u'{}'),
    Column('date_answered', types.DateTime, default=datetime.datetime.utcnow),
    )


class Question(DomainObject):

    def __init__(self, **kwargs):
        self.id=make_uuid()

    @classmethod
    def get_all(cls):
        return Session.query(cls).all()

    @classmethod
    def get(cls, question_id):
        query = Session.query(cls).autoflush(False)
        query = query.filter(cls.id == question_id)
        return query.first()


class QuestionOption(DomainObject):

    def __init__(self, **kwargs):
        self.id=make_uuid()

    @classmethod
    def get(cls, question_id):
        query = Session.query(cls).autoflush(False)
        query = query.filter(cls.question_id == question_id)
        return query.all()

    @classmethod
    def get_by_id(cls, _id):
        query = Session.query(cls).autoflush(False)
        query = query.filter(cls.id == _id)
        return query.first()


class Answer(DomainObject):

    def __init__(self, **kwargs):
        self.id=make_uuid()
        self.user_id=g.userobj.id

    @classmethod
    def get(cls, user_reference):
        query = Session.query(cls).autoflush(False)
        query = query.filter(or_(cls.user_id == user_reference,
                                cls.id == user_reference))
        return query.all()


mapper(Question, question_table, properties={})
mapper(QuestionOption, question_option_table, properties={'question': relationship (Question)})
mapper(Answer, answer_table, properties={'question': relationship (Question)})


def init_tables(self):
    metadata.create_all(model.meta.engine)
    log.info(u'Questionnaire tables created')

def del_all_tables(self):
    metadata.drop_all(model.meta.engine)
    log.info(u'Questionnaire tables deleted')
