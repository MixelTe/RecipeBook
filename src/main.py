import math
from flask import Flask, abort, jsonify, make_response, redirect, render_template, request
from flask_restful import Api
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_jwt_simple import JWTManager
from sqlalchemy import func
from data import db_session
# from api import jobs_api
# from api import users_api
# from api import login_api
# from api import users_resource
from data.users import User
from data.recipes import Recipe
from data.ingredients import Ingredient, association_table as IngredientRecipe
from data.categories import Category
import logging
logging.basicConfig(filename='recipeBook.log', format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.DEBUG, encoding="utf-8")
# from forms.departments import DepartmentForm
# from forms.job import JobForm
# from forms.login import LoginForm
# from forms.register import RegisterForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['JWT_SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
jwt_manager = JWTManager(app)
RECIPE_ON_PAGE = 20


def main():
    db_session.global_init("db/RecipeBook.db")
    # app.register_blueprint(login_api.blueprint)
    # app.register_blueprint(jobs_api.blueprint)
    # app.register_blueprint(users_api.blueprint)
    # api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    # api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')
    app.run(debug=True)


@app.route("/")
def index():
    title = request.args.get("title", None)
    categories = request.args.get("categories", None)
    ingredientsAdd = request.args.get("ingredientsAdd", None)
    ingredientsRemove = request.args.get("ingredientsRemove", None)
    page = int(request.args.get("page", 0))

    session = db_session.create_session()
    recipesQuery = session.query(Recipe)

    if (categories):
        categories = list(map(int, categories.split("-")))
        recipesQuery = recipesQuery.filter(Recipe.categories.any(Category.id.in_(categories)))
    else:
        categories = []
    if (ingredientsAdd):
        ingredientsAdd = list(map(int, ingredientsAdd.split("-")))
        # recipesQuery = recipesQuery.filter(Recipe.ingredients.any(Ingredient.id.in_(ingredientsAdd)))
        for ingredient in ingredientsAdd:
            recipesQuery = recipesQuery.filter(Recipe.ingredients.any(Ingredient.id == ingredient))
    else:
        ingredientsAdd = []
    if (ingredientsRemove):
        ingredientsRemove = list(map(int, ingredientsRemove.split("-")))
        recipesQuery = recipesQuery.filter(~Recipe.ingredients.any(Ingredient.id.in_(ingredientsRemove)))
    else:
        ingredientsRemove = []
    if (title):
        recipesQuery = recipesQuery.filter(func.lower(Recipe.title).contains(func.lower(title)))
    else:
        title = ""
    # recipes = session.query(Recipe).all()
    count = recipesQuery.count()
    pageCount = math.ceil(count / RECIPE_ON_PAGE)
    # recipes = recipesQuery.all()
    recipes = recipesQuery.slice(page * RECIPE_ON_PAGE, (page + 1) * RECIPE_ON_PAGE).all()
    # if (title):
    #     title = title.lower()
    #     recipes = list(filter(lambda el: title in el.title.lower(), recipes))

    ingredients = session.query(Ingredient).order_by(Ingredient.title).all()
    categoriesAll = session.query(Category).order_by(Category.title).all()
    data = {
        "title": title,
        "recipes": recipes,
        "ingredients": ingredients,
        "categories": categoriesAll,
        "search_categories": categories,
        "search_ingredientsAdd": ingredientsAdd,
        "search_ingredientsRemove": ingredientsRemove,
        "search_title": title,
        "count": count,
        "pageCount": pageCount,
        "page": page,
    }
    return render_template("index.html", **data)


@app.route("/about")
def about():
    return render_template("about.html", title="О")


# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user = User(
#             surname=form.surname.data,
#             name=form.name.data,
#             age=form.age.data,
#             position=form.position.data,
#             speciality=form.speciality.data,
#             address=form.address.data,
#             email=form.email.data,
#         )
#         user.set_password(form.password.data)
#         db_sess = db_session.create_session()
#         db_sess.add(user)
#         db_sess.commit()
#         return redirect('/register_success')
#     return render_template('editForm.html', title='Registration', form=form)


# @app.route("/register_success")
# def register_success():
#     return render_template('/register_success.html', title='Registration')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.email == form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember_me.data)
#             return redirect("/")
#         return render_template('login.html', title='Авторизация',
#                                message="Неправильный логин или пароль",
#                                form=form)
#     return render_template('login.html', title='Авторизация', form=form)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect("/")


# @app.route("/addjob", methods=['GET', 'POST'])
# @login_required
# def addjob():
#     form = JobForm().init()
#     if form.validate_on_submit():
#         job = Jobs(
#             job=form.job.data,
#             team_leader=form.team_leader.data,
#             work_size=form.work_size.data,
#             collaborators=",".join(map(str, form.collaborators.data)),
#             start_date=form.start_date.data,
#             end_date=form.end_date.data,
#             is_finished=form.is_finished.data,
#         )
#         db_sess = db_session.create_session()
#         db_sess.add(job)
#         db_sess.commit()
#         return redirect('/')
#     return render_template('editForm.html', title='Adding a Job', form=form)


# @app.route("/editjob/<int:id>", methods=['GET', 'POST'])
# @login_required
# def editjob(id):
#     form = JobForm().init()
#     db_sess = db_session.create_session()
#     job = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
#     if (not job):
#         abort(404)
#     if request.method == "GET":
#         form.job.data = job.job
#         form.team_leader.data = job.team_leader
#         form.work_size.data = job.work_size
#         form.collaborators.data = list(map(int, job.collaborators.split(",")))
#         form.start_date.data = job.start_date
#         form.end_date.data = job.end_date
#         form.is_finished.data = job.is_finished
#     if form.validate_on_submit():
#         job.job = form.job.data
#         job.team_leader = form.team_leader.data
#         job.work_size = form.work_size.data
#         job.collaborators = ",".join(map(str, form.collaborators.data))
#         job.start_date = form.start_date.data
#         job.end_date = form.end_date.data
#         job.is_finished = form.is_finished.data
#         db_sess.commit()
#         return redirect('/')
#     return render_template('editForm.html', title='Editing a Job', form=form)


# @app.route('/deletejob/<int:id>')
# @login_required
# def news_delete(id):
#     db_sess = db_session.create_session()
#     job = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (current_user.id == 1)).first()
#     if job:
#         db_sess.delete(job)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/')


# @app.route("/departments")
# def departments():
#     session = db_session.create_session()
#     departments = session.query(Department).all()
#     return render_template("departments.html", title="List of Departments", departments=departments)


# @app.route("/add_department", methods=['GET', 'POST'])
# @login_required
# def add_departments():
#     form = DepartmentForm().init()
#     if form.validate_on_submit():
#         department = Department(
#             title=form.title.data,
#             chief=form.chief.data,
#             members=",".join(map(str, form.members.data)),
#             email=form.email.data,
#         )
#         db_sess = db_session.create_session()
#         db_sess.add(department)
#         db_sess.commit()
#         return redirect('/departments')
#     return render_template('editForm.html', title='Adding a Department', form=form)


# @app.route("/edit_department/<int:id>", methods=['GET', 'POST'])
# @login_required
# def edit_departments(id):
#     form = DepartmentForm().init()
#     db_sess = db_session.create_session()
#     department = db_sess.query(Department).filter(Department.id == id, (Department.chief == current_user.id) | (current_user.id == 1)).first()
#     if (not department):
#         abort(404)
#     if request.method == "GET":
#         form.title.data = department.title
#         form.chief.data = department.chief
#         form.members.data = list(map(int, department.members.split(",")))
#         form.email.data = department.email
#     if form.validate_on_submit():
#         department.title = form.title.data
#         department.chief = form.chief.data
#         department.email = form.email.data
#         department.members = ",".join(map(str, form.members.data))
#         db_sess.commit()
#         return redirect('/departments')
#     return render_template('editForm.html', title='Editing a Department', form=form)


# @app.route('/delete_department/<int:id>')
# @login_required
# def delete_departments(id):
#     db_sess = db_session.create_session()
#     department = db_sess.query(Department).filter(Department.id == id, (Department.chief == current_user.id) | (current_user.id == 1)).first()
#     if department:
#         db_sess.delete(department)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/departments')


@app.errorhandler(404)
def not_found(error):
    if (request.path.startswith("/api/")):
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return render_template("error.html", title="404", text="Page not found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    if (request.path.startswith("/api/")):
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        return render_template("error.html", title="500", text="Internal Server Error"), 500


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


if __name__ == '__main__':
    main()
