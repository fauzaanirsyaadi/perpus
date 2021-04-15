from flask import jsonify

def ok(data):
  return jsonify({
    'code': 200,
    'data': data
  }), 200


def bad_request(message):
  return jsonify({
    'code': 400,
    'message': message
  }), 400


def unauthorized(message):
  return jsonify({
    'code': 401,
    'message': message
  }), 401