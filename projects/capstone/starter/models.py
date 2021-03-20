from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime


db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class AuditTrail(db.Model):

    __tablename__ = 'auditTrail'

    id = db.Column(db.Integer, primary_key=True)
    questionID = db.Column(db.Integer, db.ForeignKey('questions.id'))
    username = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    deckID = db.Column(db.Integer, db.ForeignKey('decks.id'))
    acceptance = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<AuditTrail {self.id} {self.timestamp}>'

    def __init__(self, username, acceptance):
        self.username = username
        self.acceptance = acceptance

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'questionID': self.questionID,
            'question': self.question,
            'timestamp': self.timestamp,
            'deckID': self.deckID,
            'acceptance': self.acceptance
        }

class Decks(db.Model):

    __tablename__ = 'decks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    auditTrail = db.relationship(AuditTrail,
                                 backref=db.backref('decks',
                                                    cascade='all, delete'))

    def __repr__(self):
        return f'{self.name}'

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Questions(db.Model):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    sentence = db.Column(db.String)

    auditTrail = db.relationship(AuditTrail,
                                 backref=db.backref('questions',
                                                    cascade='all, delete'))

    def __repr__(self):
        return f'<Questions {self.id} {self.question}>'

    def __init__(self, question, answer, sentence):
        self.question = question
        self.answer = answer
        self.sentence = sentence

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'sentence': self.sentence
        }