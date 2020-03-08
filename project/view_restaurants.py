from flask import Flask, current_app,  Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
import os
import time
import json

from project.models import Restaurant,Zone, Page
from . import db
from .db_queries import get_zones, update_zones, add_zone_to_db

import logging
LOG = logging.getLogger(__name__)

restaurants = Blueprint('restaurants', __name__, template_folder='templates',static_folder='static')



@restaurants.route("/zones/add", methods=["POST"])
@login_required
def add_zone():
    zone_name = request.form["name"]
    result = add_zone_to_db(zone_title=zone_name,index=0)
    return jsonify(result)


@restaurants.route("/zones/edit", methods=["GET", "POST"])
@login_required
def edit_zones():
    if request.method=="GET":
        zones_id = []
        zones = get_zones()
        for z in zones:
            zones_id.append(z.id)
        return render_template("restaurants/zone_editing.html", zones=zones, zones_id=zones_id)

    else:
        print("CHIAVI RESTITUITE")
        print(request.form.to_dict().keys())

        zones_id = request.form['new_zones_id'].split(",")
        LOG.debug("zones_id:%s" % zones_id)

        zones =  json.loads(request.form['new_zones'])
        print("ID zone da DA AGGIORNARE:")
        print(zones_id)
        print("Dizionario delle zone")
        print(zones)
        result = update_zones(zones, zones_id)
        return jsonify(result)
