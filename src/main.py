from datetime import datetime, timedelta
import math
from flask import Flask, abort, jsonify, make_response, redirect, render_template, request
from flask_restful import Api
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_jwt_simple import JWTManager
from sqlalchemy import func
from data import db_session
from data.pictures import Picture
# from api import jobs_api
# from api import users_api
# from api import login_api
# from api import users_resource
from data.users import User
from data.recipes import Recipe
from data.ingredients import Ingredient, association_table as IngredientRecipe
from data.categories import Category
# from forms.departments import DepartmentForm
# from forms.job import JobForm
from forms.login import LoginForm
from forms.register import RegisterForm
import logging
import base64


def customTime(*args):
    utc_dt = datetime.utcnow()
    utc_dt += timedelta(hours=3)
    return utc_dt.timetuple()


logging.basicConfig(
    level=logging.DEBUG,
    filename='RecipeBook.log',
    format='%(asctime)s %(levelname)-8s %(name)s     %(message)s',
    encoding="utf-8"
)
logging.getLogger("werkzeug").disabled = True
logging.Formatter.converter = customTime

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
    if __name__ == '__main__':
        app.run(debug=True)


@app.route("/")
def index():
    title = request.args.get("title", None)
    categories = request.args.get("categories", None)
    ingredientsAdd = request.args.get("ingredientsAdd", None)
    ingredientsRemove = request.args.get("ingredientsRemove", None)
    usersAdd = request.args.get("usersAdd", None)
    usersRemove = request.args.get("usersRemove", None)
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

    if (usersAdd):
        usersAdd = list(map(int, usersAdd.split("-")))
        recipesQuery = recipesQuery.filter(Recipe.creator.in_(usersAdd))
    else:
        usersAdd = []
    if (usersRemove):
        usersRemove = list(map(int, usersRemove.split("-")))
        recipesQuery = recipesQuery.filter(Recipe.creator.not_in(usersRemove))
    else:
        usersRemove = []
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
    users = session.query(User).order_by(User.name).all()
    if (current_user.is_authenticated):
        for i, user in enumerate(users):
            if (user.id == current_user.id):
                break
        user = users.pop(i)
        users.insert(0, user)
    data = {
        "title": title,
        "recipes": recipes,
        "ingredients": ingredients,
        "categories": categoriesAll,
        "search_categories": categories,
        "search_ingredientsAdd": ingredientsAdd,
        "search_ingredientsRemove": ingredientsRemove,
        "search_usersAdd": usersAdd,
        "search_usersRemove": usersRemove,
        "search_title": title,
        "count": count,
        "pageCount": pageCount,
        "page": page,
        "users": users,
    }
    return render_template("index.html", **data)


@app.route("/about")
def about():
    return render_template("about.html", title="О")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        logging.info(f"Added user: {user.name} {user.email}")
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=False)
        return redirect('/register_success')
    return render_template('editForm.html', title='Регистрация', form=form)


@app.route("/register_success")
def register_success():
    return render_template('/register_success.html', title='Регистрация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/recipe/<int:id>")
def recipe(id):
    session = db_session.create_session()
    recipe = session.query(Recipe).get(id)
    if (not recipe):
        return render_template("error.html", title="404", text="Рецепт не найден"), 404
    ingredients = session.execute("""
        select i.title, ri.count
        from RecipesIngredients as ri
        join Ingredients as i on i.id = ri.ingredient
        where ri.recipe = :recipe
        order by i.title
    """, {"recipe": recipe.id}).fetchall()
    return render_template('/recipe.html', title=recipe.title, recipe=recipe, ingredients=ingredients)


@app.route("/editRecipe/<int:id>")
@login_required
def editRecipe(id):
    session = db_session.create_session()
    recipe = session.query(Recipe).get(id)
    if (not recipe):
        return render_template("error.html", title="404", text="Рецепт не найден"), 404
    if (recipe.creator != current_user.id):
        return render_template("error.html", title="404", text="Рецепт не найден!"), 404
    ingredients = session.execute("""
        select i.title, ri.count, i.id
        from RecipesIngredients as ri
        join Ingredients as i on i.id = ri.ingredient
        where ri.recipe = :recipe
        order by i.title
    """, {"recipe": recipe.id}).fetchall()
    ingredientsAll = session.query(Ingredient).order_by(Ingredient.title).all()
    categoriesAll = session.query(Category).order_by(Category.title).all()
    data = {
        "title": recipe.title,
        "recipe": recipe,
        "ingredients": ingredients,
        "ingredientsAll": ingredientsAll,
        "categoriesAll": categoriesAll,
    }
    return render_template('/editRecipe.html', **data)


@app.route("/api/editRecipe/<int:id>", methods=['POST'])
@login_required
def editRecipeApi(id):
    session = db_session.create_session()
    recipe: Recipe = session.query(Recipe).get(id)
    if (not recipe):
        return jsonify({"result": "Not Found"}), 404
    if (recipe.creator != current_user.id):
        return jsonify({"result": "Forbidden"}), 404

    try:
        data = request.json
        recipe.title = data["title"]
        recipe.description = data["description"]
        for img in recipe.pictures:
            found = False
            for im in data["imgs"]:
                if (img.id == im["id"]):
                    found = True
                    break
            if (not found):
                recipe.pictures.remove(img)
        for img in data["imgs"]:
            if (int(img["id"]) < 0):
                picture = Picture()
                picture.img = base64.b64decode(img["img"].split(',')[1] + '==')
                if (img["preview"]):
                    picture.preview = base64.b64decode(img["preview"].split(',')[1] + '==')
                recipe.pictures.append(picture)
    except Exception as x:
        return jsonify({"result": "Bad Request"}), 400
    session.commit()

    return jsonify({"result": "OK"}), 200


@app.route("/img/<int:id>")
def img(id):
    session = db_session.create_session()
    picture: Picture = session.query(Picture).get(id)
    if (picture):
        response = make_response(picture.img)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename=f'{id}.jpg')
        return response
    abort(404)


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
        return render_template("error.html", title="404", text="Страница не найдена"), 404


@app.errorhandler(500)
@app.errorhandler(Exception)
def internal_server_error(error):
    print(error)
    logging.error(error)
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
