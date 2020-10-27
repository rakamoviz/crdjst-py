import os
import json
import flask
from flask import request, jsonify, Response
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from dateutil.parser import parse as parse_date, ParserError

class User(object):
  def __init__(self, id, username, password):
    self.id = id
    self.username = username
    self.password = password

  def __str__(self):
    return "User(id='%s')" % self.id

users = [
  User(1, 'user1', 'password'),
  User(2, 'user2', 'password'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
  user = username_table.get(username, None)
  if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
      return user

def identity(payload):
  print(payload)
  user_id = payload['identity']
  return userid_table.get(user_id, None)

def initialize (core_business, logger):
  app = flask.Flask(__name__)
  app.config['DEBUG'] = True
  app.config['SECRET_KEY'] = os.environ['ACCESS_TOKEN_SECRET']
  jwt = JWT(app, authenticate, identity)

  @app.route('/rates', methods=['GET'])
  @jwt_required()
  def obtain_rates():
    date_str = request.args.get('date')
    try:
      parse_date(date_str)
      return jsonify(core_business.obtain_rates(date_str))
    except ParserError as err:
      return Response(json.dumps({'err': 'invalid_date'}), status=400, mimetype='application/json')

  app.run()