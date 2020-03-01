# tutorial: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from werkzeug.utils import secure_filename, find_modules, import_string

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

from project.models import User

from project.auth import auth as auth_blueprint
from project.main import main as main_blueprint
from project.view_pages import pages as pages_blueprint

from project.ristoranti import ristoranti as ristoranti
from project import db_queries

import logging

def configure_logging():
    # register root logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.INFO)


def create_app():
    print("Richiamata create_app")
    app = Flask(__name__)
    Bootstrap(app)
    configure_logging()

    UPLOAD_FOLDER = 'static/uploaded_images'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    UPLOAD_FOLDER = 'static/uploaded_images'

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paris_blog_db.sqlite'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)



    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app

    app.register_blueprint(auth_blueprint)


    # blueprint for non-auth parts of app

    app.register_blueprint(main_blueprint)

    # blueprint for editable pages

    app.register_blueprint(pages_blueprint)

    return app

app = create_app()
app.run(debug=True)
