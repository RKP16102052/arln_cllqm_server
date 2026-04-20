import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    token = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    public_key = sqlalchemy.Column(sqlalchemy.Text)
    chats = sqlalchemy.Column(sqlalchemy.String)
    time_image_updated = sqlalchemy.Column(sqlalchemy.Integer)

    own_chats = orm.relationship("Chat", back_populates='created_by_user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class TempUser(SqlAlchemyBase):
    __tablename__ = 'temp_users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    token = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    verification_code = sqlalchemy.Column(sqlalchemy.Integer)
    die_time = sqlalchemy.Column(sqlalchemy.Integer)


class Chat(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    members = sqlalchemy.Column(sqlalchemy.String)
    created_by = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    is_private = sqlalchemy.Column(sqlalchemy.Boolean)
    name = sqlalchemy.Column(sqlalchemy.String)
    time_image_updated = sqlalchemy.Column(sqlalchemy.Integer)

    created_by_user = orm.relationship('User')