import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Recipes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    creator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Users.id"))
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)

    creatorUser = orm.relation('User')
    categories = orm.relation("Category", secondary="RecipesCategories")
    ingredients = orm.relation("Ingredient", secondary="RecipesIngredients")
    pictures = orm.relation("Picture", back_populates="recipe")

    def __repr__(self):
        return f"<Recipe> {self.id} {self.title}"
