import sqlalchemy as db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(250))
    date_added = db.Column(db.TIMESTAMP(), nullable=True)


class Answer_option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    answer_text = db.Column(db.String(250))


class Answer_option(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    answer_text = db.Column(db.String(250))
    date_answered = db.Column(db.TIMESTAMP(), nullable=True)

