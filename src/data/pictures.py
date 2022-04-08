import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Picture(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Pictures'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    recipeId = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Recipes.id"))
    recipe = orm.relation("Recipe", back_populates="pictures")

    def __repr__(self):
        return f"<Picture> {self.id} {self.title}"
