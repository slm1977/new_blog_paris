# tutorial: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap, WebCDN,StaticCDN

from werkzeug.utils import secure_filename, find_modules, import_string

print("Inizializzazione db")
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

print("Import User module..")
from project.models import User

print("Import auth_blueprint..")
from project.auth import auth as auth_blueprint
print("Import main_blueprint..")
from project.main import main as main_blueprint
print("Import view_pages_blueprint..")
from project.view_pages import pages as pages_blueprint
print("Import view_reastaurants_blueprint..")
from project.view_restaurants import restaurants as restaurants_blueprint

from project.ristoranti import ristoranti as ristoranti
from project import db_queries

import logging
import os
print("Fine degli import")

def configure_logging():
    # register root logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.INFO)


def create_app():
    print("Richiamata create_app")
    app = Flask(__name__)
    Bootstrap(app)
    """
    app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
    '//ajax.googleapis.com/ajax/libs/jquery/3.5.1/')
    """
    app.extensions['bootstrap']['cdns']['jquery'] = StaticCDN()

    
    configure_logging()
    # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    UPLOAD_FOLDER =  os.path.join(app.root_path, 'static/uploaded_images')
    
    
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

    # blueprint for editable restaurants
    app.register_blueprint(restaurants_blueprint)

    return app

print("Creting app...")
app = create_app()
print("app created")
#https://stackoverflow.com/questions/36649703/get-root-path-of-flask-application
#https://stackoverflow.com/questions/36649703/get-root-path-of-flask-application
#https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
app_instance_path =app.instance_path
app_root_path = app.root_path
print("app_instance_path:%s" % app_instance_path)
print("app_root_path:%s" % app_root_path)
#app.run(debug=True)
