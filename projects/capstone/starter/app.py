#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os

from flask import (Flask,
                   request,
                   abort,
                   jsonify,
                   render_template,
                   redirect,
                   url_for,
                   flash)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SubmitField,
                     SelectField,
                     TextAreaField)
from wtforms.validators import DataRequired
from models import (db,
                    AuditTrail,
                    Decks,
                    Questions)
from stanza_wrapper import stanza_wrapper
import pandas as pd



#----------------------------------------------------------------------------#
# Form.
#----------------------------------------------------------------------------#


# with Flask-WTF, each web form is represented by a class
# "MainForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class MainForm(FlaskForm):

  # https://wtforms.readthedocs.io/en/2.3.x/fields/

    note = TextAreaField('Copy below your note:', validators=[DataRequired()])
    deck_name = StringField('Put the deck name:', validators=[DataRequired()])
    submit = SubmitField('Create questions')

    deck = SelectField('User deck(s):',
                     choices=[('cpp', 'C++'),
                              ('py', 'Python'),
                              ('text', 'Plain Text')])

    show_flashcards = SubmitField('Show questions')
    remove_deck = SubmitField('Remove deck')
    edit_deck_name = SubmitField('Edit deck name')
    export_ANKI_deck = SubmitField('Export ANKI')
    export_csv = SubmitField('Export .csv')



# ----------------------------------------------------------------------------#
# TextAreaField handler.
# ----------------------------------------------------------------------------#

def text_area_field_handler(text_area_field) -> list:
    """
    Read source TextAreaField and prepare it for the future wrangling.
    It gives a list of single sentences.
    """

    try:
        raw_sentences = text_area_field.strip().split(".")
        sentences_list = list((i for i in raw_sentences if ("#" not in i) and i))
        return sentences_list

    except:
        print("Error in text_area_field_handler()")
        abort(500)


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(32)

    DB_URL = "postgresql:///herok"

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL



    # Flask-Bootstrap requires this line
    Bootstrap(app)

    #setup_db(app)

    db.app = app
    db.init_app(app)
    db.create_all()

    CORS(app)

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    #----------------------------------------------------------------------------#
    # Controllers.
    #----------------------------------------------------------------------------#

    # https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html

    @app.route('/', methods=['GET'])
    def index():
        names = ["dummyname1", "dummyname2"]
        form = MainForm()
        message = "dummymessage"
        return render_template('index.html',
                               names=names,
                               form=form,
                               message=message)

    @app.route('/', methods=['POST'])
    def create_deck():

        #TODO:
        # database route does not accept any url methods, to be fixed

        form = MainForm()

        # insert for the Stanza
        note = form.note.data.strip()

        deck_name = form.deck_name.data.strip()

        sentences_list = text_area_field_handler(note)

        stanza_wrapper(sentences_list)

        # assign output from the Stanza into database
        stanza_output = pd.read_csv("results.csv")  # TODO:#

        if form.validate():
            flash(form.errors)
            return redirect(url_for('create_deck'))

        else:
            error_in_insert = False

            try:
                new_deck = Decks(name=deck_name)
                db.session.add(new_deck)

                for index, record in stanza_output.iterrows():
                    new_question = Questions(question=record['Question'],
                                             answer=record['Answer'],
                                             sentence=record['Sentence'])
                    db.session.add(new_question)

                db.session.commit()

            except Exception as e:
                error_in_insert = True
                print(f'Exception "{e}" in create_deck()')
                db.session.rollback()
            finally:
                db.session.close()

            if not error_in_insert:
                flash('Deck ' + request.form['deck_name'] + ' was successfully created!')
                return redirect(url_for('index'))
            else:
                flash('An error occurred. Deck ' + deck_name + ' could not be created.')
                print("Error in create_deck()")
                abort(500)

    #----------------------------------------------------------------------------#
    # Error handlers for expected errors.
    #----------------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False,
                        "error": 400,
                        "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,
                        "error": 404,
                        "message": "Resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 422,
                        "message": "Unprocessable"}), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 500,
                        "message": "Internal server error"}), 500

    return app

APP = create_app()

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)