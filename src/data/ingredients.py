import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'RecipesIngredients',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('recipe', sqlalchemy.Integer, sqlalchemy.ForeignKey('Recipes.id')),
    sqlalchemy.Column('ingredient', sqlalchemy.Integer, sqlalchemy.ForeignKey('Ingredients.id')),
    sqlalchemy.Column('count', sqlalchemy.String)
)


class Ingredient(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Ingredients'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"<Ingredient> {self.id} {self.title}"
