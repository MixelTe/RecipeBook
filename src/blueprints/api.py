from flask import Blueprint, abort, jsonify, make_response, request
from flask_login import current_user, login_required
from flask_restful import abort as abort_restful, Resource, reqparse
from data import db_session
from data.users import User
from data.recipes import Recipe
from data.categories import Category
from data.ingredients import Ingredient, association_table as RecipesIngredients
from data.pictures import Picture
from sqlalchemy import func, insert
import logging
import base64


blueprint = Blueprint(
    'api',
    __name__,
    template_folder='templates'
)



@blueprint.route("/api/editRecipe/<int:id>", methods=['POST'])
@login_required
def editRecipe(id):
    session = db_session.create_session()
    if (id == 0):
        recipe = Recipe(creator=current_user.id)
        session.add(recipe)
    else:
        recipe: Recipe = session.query(Recipe).get(id)
        if (not recipe):
            return jsonify({"result": "Not Found"}), 404
        if (recipe.creator != current_user.id):
            return jsonify({"result": "Forbidden"}), 404

    try:
        data = request.json
        recipe.title = data["title"]
        recipe.description = data["description"]
        for i in range(len(recipe.pictures) - 1, -1, -1):
            img = recipe.pictures[i]
            found = False
            for im in data["imgs"]:
                if (img.id == int(im["id"])):
                    found = True
                    break
            if (not found):
                recipe.pictures.remove(img)
                session.delete(img)
        for img in data["imgs"]:
            if (int(img["id"]) < 0):
                picture = Picture()
                picture.img = base64.b64decode(img["img"].split(',')[1] + '==')
                if (img["preview"]):
                    picture.preview = base64.b64decode(img["preview"].split(',')[1] + '==')
                recipe.pictures.append(picture)
        for i in range(len(recipe.ingredients) - 1, -1, -1):
            ingredient = recipe.ingredients[i]
            recipe.ingredients.remove(ingredient)
        for i in range(len(recipe.categories) - 1, -1, -1):
            category = recipe.categories[i]
            recipe.categories.remove(category)
        session.commit()
        for el in data["ingredients"]:
            id, count = el["id"], el["count"]
            ingredient = session.query(Ingredient).get(id)
            if (ingredient):
                session.execute(
                    insert(RecipesIngredients),
                    {"recipe": recipe.id, "ingredient": ingredient.id, "count": count}
                )
        for id in data["categories"]:
            category = session.query(Category).get(id)
            if (category):
                recipe.categories.append(category)
        session.commit()
    except Exception as x:
        return jsonify({"result": "Bad Request"}), 400
    if (id == 0):
        logging.info(f"Added recipe: {recipe.id} {recipe.title}")
    else:
        logging.info(f"Updated recipe: {recipe.id} {recipe.title}")

    return jsonify({"result": "OK", "id": recipe.id}), 200


@blueprint.route("/img/<int:id>")
def img(id):
    session = db_session.create_session()
    picture: Picture = session.query(Picture).get(id)
    if (picture):
        p = request.args.get("p")
        img = picture.img
        if (p is not None and picture.preview):
            img = picture.preview
        response = make_response(img)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'inline', filename=f'recipe-img-{id}.jpg')
        response.headers.set('Cache-Control', 'public,max-age=31536000,immutable')
        return response
    abort(404)


@blueprint.route("/api/deleteRecipe/<int:id>", methods=['POST'])
@login_required
def deleteRecipe(id):
    session = db_session.create_session()
    recipe: Recipe = session.query(Recipe).get(id)
    if (not recipe):
        return jsonify({"result": "Not Found"}), 404
    if (recipe.creator != current_user.id):
        return jsonify({"result": "Forbidden"}), 404

    recipe.deleted = True
    session.commit()
    logging.info(f"Deleted recipe: {recipe.id} {recipe.title}")

    return jsonify({"result": "OK"}), 200


@blueprint.route("/api/restoreRecipe/<int:id>", methods=['POST'])
@login_required
def restoreRecipe(id):
    session = db_session.create_session()
    recipe: Recipe = session.query(Recipe).get(id)
    if (not recipe):
        return jsonify({"result": "Not Found"}), 404
    if (recipe.creator != current_user.id):
        return jsonify({"result": "Forbidden"}), 404

    recipe.deleted = False
    session.commit()
    logging.info(f"Restored recipe: {recipe.id} {recipe.title}")

    return jsonify({"result": "OK"}), 200


parser_title = reqparse.RequestParser()
parser_title.add_argument("title", required=True)


class IngredientListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        ingredients = db_sess.query(Ingredient).all()
        return jsonify([item.to_dict(only=("id", "title")) for item in ingredients])

    def post(self):
        args = parser_title.parse_args()
        db_sess = db_session.create_session()
        ingredient = Ingredient(title=str(args["title"]))
        db_sess.add(ingredient)
        db_sess.commit()
        return jsonify({'success': 'OK', "id": ingredient.id})


class CategoryListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        categories = db_sess.query(Category).all()
        return jsonify([item.to_dict(only=("id", "title")) for item in categories])

    def post(self):
        args = parser_title.parse_args()
        db_sess = db_session.create_session()
        category = Category(title=str(args["title"]))
        db_sess.add(category)
        db_sess.commit()
        return jsonify({'success': 'OK', "id": category.id})
