import os
from flask import (Flask,
                   request,
                   jsonify,
                   abort)
from sqlalchemy import exc
import json
from flask_cors import (CORS,
                        cross_origin)

from .database.models import (db_drop_and_create_all,
                              setup_db,
                              Drink)
from .auth.auth import (AuthError,
                        requires_auth)

app = Flask(__name__)
setup_db(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

'''
!! NOTE THE LINE BELOW MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

'''
GET /drinks
public endpoint, fetches all drinks with a short description;
'''
@app.route('/drinks')
@cross_origin()
def get_drinks():
    try:
        drinks_short_data = [drink.short() for drink in Drink.query.all()]
        return json.dumps({'success': True,
                           'drinks': drinks_short_data}), 200
    except:
        return json.dumps({'success': False,
                           'error': "Failure during short drink data representation."}), 500

'''
GET /drinks-detail
fetches all drinks with a long description;
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-details')
@cross_origin()
def get_drinks_detailed(jwt):
    try:
        drinks_long_data = [drink.long() for drink in Drink.query.all()]
        return json.dumps({'success': True,
                           'drinks': drinks_long_data}), 200
    except:
        return json.dumps({'success': False,
                           'error': "Failure during long drink data representation."}), 500

'''
POST /drinks
insert an array containing the newly created drink data
'''
@app.route('/drinks',
           methods=['POST'])
@requires_auth('post:drinks')
@cross_origin()
def add_drink(jwt):

    body = request.get_json()

    if body is None: abort(422)

    try:
        title = body.get('title')
        recipe = json.dumps(body.get('recipe'))
        drink = Drink(title = title,
                      recipe = recipe)
        drink.insert()
        drink_long_data = drink.long()
        return json.dumps({'success': True,
                           'drink': drink_long_data}), 200
    except:
        return json.dumps({'success': False,
                           'error': "An error occurred during drink data insertion"}), 500

'''
PATCH /drinks/<id> where <id> is the existing model id
update drink data if it exists
'''
@app.route('/drinks/<id>',
           methods=['PATCH'])
@requires_auth('patch:drinks')
@cross_origin()
def edit_drinks(jwt, id):
    try:
        data = dict(request.form or request.json or request.data)
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:

            if data.get('title'): drink.title = data.get('title')

            if data.get('recipe'): recipe = data.get('recipe')
            else: recipe = drink.recipe

            if type(recipe) == str: drink.recipe = recipe
            else: drink.recipe = json.dumps(recipe)

            drink.update()
            drink_long_data = [drink.long()]
            return json.dumps({'success': True,
                               'drinks': drink_long_data}), 200
        else:
            return json.dumps({'success': False,
                               'error': 'Drink cannot be edited (#' + id + ' not found)'}), 404
    except:
        return json.dumps({'success': False,
                           'error': "An error occurred during drink data update"}), 500

'''
DELETE /drinks/<id> where <id> is the existing model id
remove drink data
'''
@app.route('/drinks/<id>',
           methods=['DELETE'])
@requires_auth('patch:drinks')
@cross_origin()
def delete_drink(jwt, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:
            drink.delete()
            return json.dumps({'success': True,
                               'drink': id}), 200
        else:
            return json.dumps({'success': False,
                               'error': 'Drink cannot be deleted (#' + id + ' not found)'}), 404
    except:
        return json.dumps({'success': False,
                           'error': "An error occurred during drink data deletion"}), 500

'''
error handlers using the @app.errorhandler(error) decorator
'''

@app.errorhandler(AuthError)
def autherror(error):
    error_code = error.status_code
    return jsonify({'success': False,
                    'error': error_code,
                    'message': error.error['description']}), error_code

@app.errorhandler(400)
def badrequest(error):
    return jsonify({"success": False,
                    "error": 400,
                    "message": "check the request"}), 400

@app.errorhandler(404)
def resourcenotfound(error):
    return jsonify({"success": False,
                    "error": 404,
                    "message": "resource not found"}), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False,
                    "error": 422,
                    "message": "unprocessable entity"}), 422