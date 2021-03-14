#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  cors = CORS(app, resources={r"*": {"origins": "*"}})

  return app

APP = create_app()


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#







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

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)