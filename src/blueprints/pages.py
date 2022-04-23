from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from data import db_session
from data.users import User
from data.recipes import Recipe
from data.categories import Category
from data.ingredients import Ingredient
from sqlalchemy import func
from forms.register import RegisterForm
from forms.login import LoginForm
import math
import logging


blueprint = Blueprint(
    'pages',
    __name__,
    template_folder='templates'
)
RECIPE_ON_PAGE = 20


@blueprint.route("/")
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
    if (current_user.is_authenticated and request.args.get("d") is not None):
        recipesQuery = recipesQuery.filter(Recipe.deleted == True)
        if (current_user.id != 1):
            recipesQuery = recipesQuery.filter(Recipe.creator == current_user.id)
    else:
        recipesQuery = recipesQuery.filter(Recipe.deleted == False)

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
        "title": "Книга рецептов",
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


@blueprint.route("/about")
def about():
    return render_template("about.html", title="О")


@blueprint.route("/register", methods=['GET', 'POST'])
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


@blueprint.route("/register_success")
def register_success():
    return render_template('/register_success.html', title='Регистрация')


@blueprint.route('/login', methods=['GET', 'POST'])
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


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route("/recipe/<int:id>")
def recipe(id):
    session = db_session.create_session()
    recipe: Recipe = session.query(Recipe).get(id)
    if (not recipe):
        return render_template("error.html", title="404", text="Рецепт не найден"), 404
    if (recipe.deleted):
        if ((not current_user.is_authenticated) or (current_user.id not in [recipe.creator, 1])):
            return render_template("error.html", title="404", text="Рецепт не найден"), 404
    ingredients = session.execute("""
        select i.title, ri.count
        from RecipesIngredients as ri
        join Ingredients as i on i.id = ri.ingredient
        where ri.recipe = :recipe
        order by i.title
    """, {"recipe": recipe.id}).fetchall()
    return render_template('/recipe.html', title=recipe.title, recipe=recipe, ingredients=ingredients)


@blueprint.route("/editRecipe/<int:id>")
@login_required
def editRecipe(id):
    session = db_session.create_session()
    if (id == 0):
        recipe = Recipe(id=0, title="", description="")
    else:
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
        "title": "Добавление рецепта" if (id == 0) else recipe.title,
        "recipe": recipe,
        "ingredients": ingredients,
        "ingredientsAll": ingredientsAll,
        "categoriesAll": categoriesAll,
    }
    return render_template('/editRecipe.html', **data)
