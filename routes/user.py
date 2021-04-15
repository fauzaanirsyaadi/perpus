from flask import Blueprint, request
from ..controllers.user import UserController

user = Blueprint('user', __name__)

@user.route('/fetch', methods=['GET'])
def fetch():
  user_controller = UserController()
  return user_controller.fetch()

@user.route('/create', methods=['POST'])
def create():
  payload = request.get_json()
  user_controller = UserController()
  return user_controller.create(payload=payload)