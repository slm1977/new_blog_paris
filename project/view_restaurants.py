from flask import Flask, current_app,  Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user
import os
import time
from .models import Restaurant,Zone
from . import db
#from .db_queries import

import logging
LOG = logging.getLogger(__name__)

restaurants = Blueprint('restaurants', __name__,template_folder='templates',static_folder='static')

@restaurants.route("/restaurants/add")
@login_required
def create_new_restaurant():
    return "To be implemented"
