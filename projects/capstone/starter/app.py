#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired



from models import setup_db, AuditTrail, Decks, Questions

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#



# with Flask-WTF, each web form is represented by a class
# "MainForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class MainForm(FlaskForm):
    note = StringField('Copy below your note:', validators=[DataRequired()])
    deck_name = StringField('Put the deck name:', validators=[DataRequired()])
    submit = SubmitField('Create questions')

    deck = SelectField(
        'User deck(s):',
        choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    )

    show_flashcards = SubmitField('Show questions')
    remove_deck = SubmitField('Remove deck')
    edit_deck_name = SubmitField('Edit deck name')
    export_ANKI_deck = SubmitField('Export ANKI')
    export_csv = SubmitField('Export .csv')



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)

  # Flask-WTF requires an encryption key - the string can be anything
  app.config['SECRET_KEY'] = 'dummykey'

  # Flask-Bootstrap requires this line
  Bootstrap(app)

  setup_db(app)

  CORS(app)

  cors = CORS(app, resources={r"*": {"origins": "*"}})




#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html

  @app.route('/', methods=['GET', 'POST'])
  def index():
      names = ["dummyname1", "dummyname2"]
      form = MainForm()
      message = "dummymessage"
      return render_template('index.html',
                             names=names,
                             form=form,
                             message=message)


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