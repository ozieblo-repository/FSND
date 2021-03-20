from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime


db = SQLAlchemy()
'''
setup_db(app) binds a flask application and a SQLAlchemy service
'''

def setup_db(app):



    if config is None:
        app.config.from_object(config.BaseConfig)
    else:
        app.config.from_object(config)

    db.app = app
    db.init_app(app)
    db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class AuditTrail(db.Model):

    __tablename__ = 'AuditTrail'

    questionID = db.Column(db.Integer, db.ForeignKey('Questions.questionID'), primary_key=True)
    username = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deckID = db.Column(db.Integer, db.ForeignKey('Decks.deckID'))
    acceptance = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<AuditTrail {self.recordID} {self.timestamp}>'

    def __init__(self, username, timestamp, deckID, acceptance):
        self.username = username
        self.timestamp = timestamp
        self.deckID = deckID
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
            'questionID': self.questionID,
            'question': self.question,
            'timestamp': self.timestamp,
            'deckID': self.deckID,
            'acceptance': self.acceptance
        }

class Decks(db.Model):

    __tablename__ = 'Decks'

    deckID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    auditTrail = db.relationship(AuditTrail,
                                 backref=db.backref('Decks',
                                                    cascade='all, delete'))

    def __repr__(self):
        return f'<Decks {self.deckID} {self.name}>'

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
            'deckID': self.deckID,
            'name': self.name
        }

class Questions(db.Model):

    __tablename__ = 'Questions'

    questionID = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    sentence = db.Column(db.String)

    auditTrail = db.relationship(AuditTrail,
                                 backref=db.backref('Questions',
                                                    cascade='all, delete'))

    def __repr__(self):
        return f'<Questions {self.questionID} {self.question}>'

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
            'questionID': self.questionID,
            'question': self.question,
            'answer': self.answer,
            'sentence': self.sentence
        }