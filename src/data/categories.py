import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'RecipesCategories',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('recipe', sqlalchemy.Integer, sqlalchemy.ForeignKey('Recipes.id')),
    sqlalchemy.Column('category', sqlalchemy.Integer, sqlalchemy.ForeignKey('Categories.id'))
)


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"<Category> {self.id} {self.title}"
