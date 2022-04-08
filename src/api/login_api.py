from flask import Blueprint, jsonify, request
from data import db_session
from data.users import User
from api.create_jwt import create_jwt

blueprint = Blueprint(
    'login_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/login', methods=['POST'])
def login():
    json: dict = request.get_json()
    if (not json):
        return jsonify({"error": "Empty request"})

    email = json.get('email', None)
    password = json.get('password', None)

    if (not email):
        return jsonify({"error": "Missing email parameter"})
    if (not password):
        return jsonify({"error": "Missing password parameter"})

    email = str(email)
    password = str(password)

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        return jsonify({'jwt': create_jwt(identity=user.id)})
    return jsonify({"error": "Bad username or password"})
