import json
import flask
from flask import request, jsonify, Response
from dateutil.parser import parse as parse_date, ParserError

def initialize (core_business, logger):
  app = flask.Flask(__name__)
  app.config["DEBUG"] = True

  @app.route('/rates', methods=['GET'])
  def obtain_rates():
    date_str = request.args.get('date')
    try:
      parse_date(date_str)
      return jsonify(core_business.obtain_rates(date_str))
    except ParserError as err:
      return Response(json.dumps({'err': 'invalid_date'}), status=400, mimetype='application/json')

  app.run()