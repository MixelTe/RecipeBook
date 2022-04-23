from flask import Flask, jsonify, make_response, redirect, render_template, request
from flask_restful import Api
from flask_login import LoginManager
from flask_jwt_simple import JWTManager
from data import db_session
from blueprints.api import blueprint as blueprint_api, IngredientListResource, CategoryListResource
from blueprints.pages import blueprint as blueprint_pages
from blueprints.other import blueprint as blueprint_other
from data.users import User
import logging
from logger import setLogging
import traceback


setLogging()
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['JWT_SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
jwt_manager = JWTManager(app)


def main():
    db_session.global_init("db/RecipeBook.db")
    app.register_blueprint(blueprint_api)
    app.register_blueprint(blueprint_pages)
    app.register_blueprint(blueprint_other)
    api.add_resource(IngredientListResource, '/api/ingredients')
    api.add_resource(CategoryListResource, '/api/categories')
    if __name__ == '__main__':
        app.run(debug=True)


@app.errorhandler(404)
def not_found(error):
    if (request.path.startswith("/api/")):
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return render_template("error.html", title="404", text="Страница не найдена"), 404


@app.errorhandler(500)
@app.errorhandler(Exception)
def internal_server_error(error):
    print(error)
    logging.error(f'{error}\n{traceback.format_exc()}')
    if (request.path.startswith("/api/")):
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        return render_template("error.html", title="500", text="Произошла ошибка на сервере"), 500


@app.errorhandler(401)
def unauthorized(error):
    if (request.path.startswith("/api/")):
        return make_response(jsonify({'error': 'Unauthorized'}), 401)
    else:
        return redirect("/login")


@jwt_manager.expired_token_loader
def expired_token_loader():
    return jsonify({'error': 'The JWT has expired'}), 401


@jwt_manager.invalid_token_loader
def invalid_token_loader(error):
    return jsonify({'error': 'Invalid JWT'}), 401


@jwt_manager.unauthorized_loader
def unauthorized_loader(error):
    return jsonify({'error': 'Missing Authorization Header'}), 401


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


main()
