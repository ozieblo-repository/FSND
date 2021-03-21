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
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired
from models import (db,
                    AuditTrail,
                    Decks,
                    Questions)
from stanza_wrapper import stanza_wrapper

from wtforms.ext.sqlalchemy.fields import QuerySelectField


#----------------------------------------------------------------------------#
# Forms.
#----------------------------------------------------------------------------#

class CreateQuestions(FlaskForm):
    # https://wtforms.readthedocs.io/en/2.3.x/fields/

    note = wtforms.TextAreaField('Copy below your note:', validators=[DataRequired()])
    deck_name = wtforms.StringField('Put the deck name:', validators=[DataRequired()])
    submit = wtforms.SubmitField('Create questions')

def dropdown_query():
    return Decks.query


class SelectDeck(FlaskForm):
    # https://stackoverflow.com/questions/33832940/flask-how-to-populate-select-field-in-wtf-form-when-database-files-is-separate
    pick_the_deck = QuerySelectField(query_factory=dropdown_query,
                                         label="Decks:",
                                         allow_blank=True,
                                         blank_text="No deck have been created yet!")

# https://stackoverflow.com/questions/49037015/is-posible-to-render-wtf-form-field-with-out-label
class NoLabelMixin(object):
    def __init__(self, *args, **kwargs):
        super(NoLabelMixin, self).__init__(*args, **kwargs)
        for field_name in self._fields:
            field_property = getattr(self, field_name)
            field_property.label = ""

class MainForm(FlaskForm):
    # https://dev.to/sampart/combining-multiple-forms-in-flask-wtforms-but-validating-independently-cbm
    create_questions = wtforms.FormField(CreateQuestions)
    dropdown_value = wtforms.FormField(SelectDeck)

class MainFormNoLabel(NoLabelMixin, MainForm):
    pass

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

    db.app = app
    db.init_app(app)
    db.drop_all()
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
        form = MainFormNoLabel()
        message = "dummymessage"
        return render_template('index.html',
                               names=names,
                               form=form,
                               message=message)

    @app.route('/', methods=['POST'])
    def create_deck():

        form = MainFormNoLabel()

        # insert for the Stanza
        note = form.create_questions.note.data.strip()

        deck_name = form.create_questions.deck_name.data.strip()

        sentences_list = text_area_field_handler(note)

        # assign output from the Stanza into database
        stanza_output = stanza_wrapper(sentences_list)

        if form.validate():
            flash(form.errors)
            return redirect(url_for('/')) ###### !!!!

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
                    db.session.flush()

                    new_record = AuditTrail(username="testUser",
                                            acceptance=False)

                    new_record.questionID = new_question.id
                    new_record.deckID = new_deck.id

                    db.session.add(new_record)

                db.session.commit()

            except Exception as e:
                error_in_insert = True
                print(f'Exception "{e}" in create_deck()')
                db.session.rollback()
            finally:
                db.session.close()

            if not error_in_insert:
                return redirect(url_for('index'))
            else:
                print("Error in create_deck()")
                abort(500)


    #@app.route('/delete', methods=['GET'])
    #def delete_deck():
    #    form = MainFormNoLabel()
    #    return render_template(form=form)

    # background process happening without any refreshing
    @app.route('/background_process_test')
    def background_process_test():
        print("Hello")

        try:
            form = MainFormNoLabel()

            print(form.dropdown_value)


            if form.dropdown_value.validate():
                print(''.format((form.dropdown_value.pick_the_deck.data)))




            deck_to_remove = Decks.query.filter(Decks.name == deck_name).one_or_none()
            records_to_remove = AuditTrail.query.filter(AuditTrail.deckID == deck_to_remove.id).all()
            questions_to_remove = Questions.query.filter(Questions.deckID in records_to_remove.questionID).all()

            print(deck_to_remove)
            print(questions_to_remove)
            print(records_to_remove)

            deck_to_remove.delete()
            questions_to_remove.delete()
            records_to_remove.delete()

            print("Kabanos")

        except:
            db.session.rollback()
        finally:
            db.session.close()

        print("Goodbye")

        return ("nothing")



    @app.route('/delete', methods=['POST'])
    def remove_deck():

        form = MainFormNoLabel()

        try:
            deck_name = form.dropdown_value.pick_the_deck.data.strip()
            deck_to_remove = Decks.query.filter(Decks.name == deck_name).one_or_none()
            records_to_remove = AuditTrail.query.filter(AuditTrail.deckID == deck_to_remove.id).all()
            questions_to_remove = Questions.query.filter(Questions.deckID in records_to_remove.questionID).all()

            deck_to_remove.delete()
            questions_to_remove.delete()
            records_to_remove.delete()

        except:
            db.session.rollback()
        finally:
           db.session.close()

        return redirect(url_for('/'))



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
    APP.run(host='0.0.0.0',
            port=8080,
            debug=True)

# https://bitadj.medium.com/completely-uninstall-and-reinstall-psql-on-osx-551390904b86
# https://medium.com/@richardgong/how-to-upgrade-postgres-db-on-mac-homebrew-99516db3e57f
# https://stackoverflow.com/questions/61899041/how-to-fix-the-error-permission-denied-apply2files-usr-local-lib-node-modul