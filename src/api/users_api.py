from flask import Blueprint, jsonify, request
from flask_jwt_simple import jwt_required, get_jwt_identity
from data import db_session
from data.users import User


blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users': [item.to_dict(only=("id", "name", "surname", "position", "email")) for item in users]
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    fields = ("surname", "name", "age", "position", "speciality", "address", "email", "password")
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in fields):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    try:
        if (db_sess.query(User).filter_by(email=str(request.json["email"])).first()):
            return jsonify({'error': 'Email address already taken'})
        user = User(
            surname=str(request.json["surname"]),
            name=str(request.json["name"]),
            age=int(request.json["age"]),
            position=str(request.json["position"]),
            speciality=str(request.json["speciality"]),
            address=str(request.json["address"]),
            email=str(request.json["email"])
        )
        user.set_password(str(request.json["password"]))
        db_sess.add(user)
        db_sess.commit()
    except Exception:
        return jsonify({'error': 'Bad request'})
    return jsonify({'success': 'OK', "user_id": user.id})


@blueprint.route('/api/users/<int:id>')
def get_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if (not user):
        return jsonify({'error': 'Not found'})
    fields = ("id", "surname", "name", "age", "position", "speciality", "address", "email")
    return jsonify(
        {
            'user': user.to_dict(only=fields)
        }
    )


@blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if (not user):
        return jsonify({'error': 'Not found'})
    userId = get_jwt_identity()
    if (user.id != userId and userId != 1):
        return jsonify({'error': 'Forbidden'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:id>', methods=['PUT'])
def edit_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    fields = ("surname", "name", "age", "position", "speciality", "address", "email", "password")
    if (not user):
        return jsonify({'error': 'Not found'})
    userId = get_jwt_identity()
    if (user.id != userId and userId != 1):
        return jsonify({'error': 'Forbidden'})
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in fields):
        return jsonify({'error': 'Bad request'})
    try:
        if ("surname" in request.json):
            user.surname = str(request.json["surname"])
        if ("name" in request.json):
            user.name = str(request.json["name"])
        if ("age" in request.json):
            user.age = int(request.json["age"])
        if ("position" in request.json):
            user.position = str(request.json["position"])
        if ("speciality" in request.json):
            user.speciality = str(request.json["speciality"])
        if ("address" in request.json):
            user.address = str(request.json["address"])
        if ("email" in request.json):
            if (db_sess.query(User).filter_by(email=str(request.json["email"])).first()):
                return jsonify({'error': 'Email address already taken'})
            user.email = str(request.json["email"])
        if ("password" in request.json):
            user.set_password(str(request.json["password"]))
        db_sess.commit()
    except Exception:
        return jsonify({'error': 'Bad request'})
    return jsonify({'success': 'OK'})
