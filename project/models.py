from flask_login import UserMixin

# libreria python che interagisce coi DB
from sqlalchemy.sql import expression

from project import db

class User(UserMixin, db.Model):
    __table_name__ = "User"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Page(UserMixin, db.Model):
    __table_name__ = "Page"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    menu_title = db.Column(db.String(1000), unique=True)
    path = db.Column(db.String(1000), unique=True)
    index = db.Column(db.Integer)
    visible = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    type = db.Column(db.Integer)
    deleted = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    
    def __repr__(self): 
        return "<Page: %s index:%s menu_title:%s filepath:%s>" % (self.id, self.index, self.menu_title, self.path)


class Zone(UserMixin, db.Model):
    __table_name__ = "Zone"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(200), unique=True)
    index = db.Column(db.Integer)
    restaurants = db.relationship('Restaurant', backref='zone', lazy=True)
    visible = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    deleted = db.Column(db.Boolean, server_default=expression.false(), nullable=False)


class Restaurant(UserMixin, db.Model):
    __table_name__ = "Restaurant"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    topic = db.Column(db.String(100))
    description = db.Column(db.String(1500))
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))
    index = db.Column(db.Integer)
    orari = db.Column(db.String(100))
    visible = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    deleted = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    images = db.Column(db.String(500))

#https://stackoverflow.com/questions/46055661/flask-many-to-many-relation-leads-to-multiple-classes-found-for-path
#https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
#https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
#https://docs.sqlalchemy.org/en/13/orm/join_conditions.html
#https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
#https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_working_with_joins.htm
#https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_using_multiple_tables.htm
