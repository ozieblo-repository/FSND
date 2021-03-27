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
from .models import (db,
                     Decks,
                     AuditTrail,
                     Questions)
from .stanza_wrapper import stanza_wrapper
from wtforms.ext.sqlalchemy.fields import QuerySelectField

#----------------------------------------------------------------------------#
# Forms.
#----------------------------------------------------------------------------#

class CreateQuestions(FlaskForm):
    #### https://wtforms.readthedocs.io/en/2.3.x/fields/
    note = wtforms.TextAreaField('Copy below your note:', validators=[DataRequired()])
    deck_name = wtforms.StringField('Put the deck name:', validators=[DataRequired()])

class SubmitNote(FlaskForm):
    submit = wtforms.SubmitField()

def dropdown_query():
    return Decks.query.order_by(Decks.id.desc())

class SelectDeck(FlaskForm):
    #### https://stackoverflow.com/questions/33832940/flask-how-to-populate-select-field-in-wtf-form-when-database-files-is-separate
    pick_the_deck = QuerySelectField(query_factory=dropdown_query,
                                     label="Decks:",
                                     #allow_blank=True,
                                     #blank_text="Select the deck",
                                     id="removedeck" )

#### https://stackoverflow.com/questions/49037015/is-posible-to-render-wtf-form-field-with-out-label
class NoLabelMixin(object):
    def __init__(self, *args, **kwargs):
        super(NoLabelMixin, self).__init__(*args, **kwargs)
        for field_name in self._fields:
            field_property = getattr(self, field_name)
            field_property.label = ""

class MainForm(FlaskForm):
    #### https://dev.to/sampart/combining-multiple-forms-in-flask-wtforms-but-validating-independently-cbm
    create_questions = wtforms.FormField(CreateQuestions)
    submit_note = wtforms.FormField(SubmitNote)

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

def drop_everything():
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()

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

    drop_everything()

    db.drop_all()
    db.create_all()

    CORS(app)

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    #----------------------------------------------------------------------------#
    # Controllers.
    #----------------------------------------------------------------------------#

    #### https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html

    @app.route('/', methods=['GET'])
    def index():
        form = MainFormNoLabel()

        questions = Questions.query.all()

        return render_template('index.html',
                               form=form,
                               questions=questions)

    @app.route('/', methods=['POST'])
    def manage_deck():

        form = MainFormNoLabel()

        # insert for the Stanza
        note = form.create_questions.note.data.strip()

        deck_name = form.create_questions.deck_name.data.strip()

        sentences_list = text_area_field_handler(note)

        # assign output from the Stanza into database
        stanza_output = stanza_wrapper(sentences_list)

        if form.validate():
            flash(form.errors)
            return redirect(url_for('/'))

        else:
            error_in_insert = False

            try:

                new_deck = Decks(name=deck_name)
                db.session.add(new_deck)

                for index, record in stanza_output.iterrows():

                    new_record = AuditTrail(username="testUser")

                    db.session.add(new_record)

                    new_question = Questions(question=record['Question'],
                                             answer=record['Answer'],
                                             sentence=record['Sentence'],
                                             auditTrail=new_record)

                    db.session.add(new_question)



                    # https://stackoverflow.com/questions/16433338/inserting-new-records-with-one-to-many-relationship-in-sqlalchemy
                    new_deck.auditTrail.append(new_record)

                db.session.commit()

            except Exception as e:
                error_in_insert = True
                print(f'Exception "{e}" in manage_deck()')
                db.session.rollback()
            finally:
                db.session.close()

            if not error_in_insert:
                return redirect(url_for('index'))
            else:
                print("Error in manage_deck()")
                abort(500)

    @app.route('/questionremove/<questionId>', methods=['DELETE'])
    def questionremove(questionId):

        try:
            question_to_remove = Questions.query.filter(Questions.id == questionId).one_or_none()
            question_to_remove.delete()
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return jsonify({'success': True,
                        'deleted': questionId,
                        'message': "Question successfully deleted"})

    @app.route('/managedecks', methods=['GET'])
    def managedecks():
        form = SelectDeck()
        questions = Questions.query.order_by('id').all()
        return render_template('managedecks.html',
                               form=form,
                               questions=questions)

    @app.route('/deckremove/<deckId>', methods=['DELETE'])
    def removedeck(deckId):

        try:
            deck_to_remove = Decks.query.filter(Decks.id == deckId).one_or_none()
            deck_to_remove.delete()
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return redirect("/managedecks")

# https://knowledge.udacity.com/questions/419323
    @app.route("/updatesentence", methods=["POST"])
    def updatesentence():

        questionId = request.form.get("oldsentenceid")
        newsentence = request.form.get("newsentence")
        questions = Questions.query.filter(Questions.id==questionId).first()
        questions.sentence = newsentence
        db.session.commit()

        return redirect("/managedecks")

    @app.route("/updatequestion", methods=["POST"])
    def updatequestion():

        questionId = request.form.get("oldquestionid")
        newquestion = request.form.get("newquestion")
        questions = Questions.query.filter(Questions.id==questionId).first()
        questions.question = newquestion
        db.session.commit()

        return redirect("/managedecks")

    @app.route("/updateanswer", methods=["POST"])
    def updateanswer():

        questionId = request.form.get("oldanswerid")
        newanswer = request.form.get("newanswer")
        questions = Questions.query.filter(Questions.id==questionId).first()
        questions.answer = newanswer
        db.session.commit()

        return redirect("/managedecks")



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

app = create_app()

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=8080,
            debug=True)

# https://bitadj.medium.com/completely-uninstall-and-reinstall-psql-on-osx-551390904b86
# https://medium.com/@richardgong/how-to-upgrade-postgres-db-on-mac-homebrew-99516db3e57f
# https://stackoverflow.com/questions/61899041/how-to-fix-the-error-permission-denied-apply2files-usr-local-lib-node-modul