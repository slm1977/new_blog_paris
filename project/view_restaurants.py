from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user

import os
import time
import json

from project.models import Restaurant,Zone, Page
from . import db
from .db_queries import get_zones, update_zones, add_zone_to_db,  \
                        update_restaurant, add_restaurant_to_db, delete_restaurant, get_next_restaurant_id

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


@restaurants.route("/restaurant/edit/<restaurant_id>/", methods=["GET"])
@login_required
def edit_restaurant(restaurant_id):
    LOG.debug("Cerco di caricare ristorante con id:%s" % restaurant_id)
    if int(restaurant_id)<=0:
        return redirect(request.referrer)
        
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()

    
    zones = get_zones()
    return render_template("restaurants/restaurant_editing.html", 
    restaurant=restaurant, zones=zones, restaurant_id=restaurant.id)

@restaurants.route("/restaurant/add/", methods=["GET"])
@login_required
def add_restaurant():
    zones = get_zones()
    new_restaurant_id = get_next_restaurant_id()
    return render_template("restaurants/restaurant_editing.html", restaurant=None, 
    zones=zones, restaurant_id=new_restaurant_id)


@restaurants.route("/restaurant/remove/<restaurant_id>/", methods=["GET"])
@login_required
def remove_restaurant(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    if restaurant!=None:
        delete_restaurant(restaurant_id)
        return redirect(url_for("main.caricaLibroRistorante2", zone_id=restaurant.zone_id))
    return redirect("/")

@restaurants.route("/restaurants/save", methods=["POST"])
@login_required
def save_restaurant():
    print("Saving restaurant...")
    name = request.form.get('title')
    rest_id = request.form.get('id')
    visible = True if request.form.get('visible')=="true" else False
    zone_id = request.form.get('zone')
    address = request.form.get('address')
    orari = request.form.get('orari')
    topic = request.form.get('topic')
    description = request.form.get('description')
    index = 1 # default... non utilizzato
    latitude =  request.form.get('latitude')
    longitude = request.form.get('longitude')
    deleted = False
    images = request.form.get('images')

    print("Lat:%s Long:%s Topic:%s Desc:%s\nOrari:%s Address:%s Zone:%s Title:%s Id:%s visible:%s\nimages:%s" % 
    (latitude, longitude,topic, description, orari, address,zone_id, name , rest_id, visible, images))

    res = update_restaurant(rest_id, name, address, topic, description, zone_id, orari, 
                            visible, latitude, longitude, images, index)
    if res!=None:
        result = {"success" : True,
                    "message" : "Ristorante salvato con successo lat:%s lon:%s" % (latitude, longitude) ,
                    "restaurant_id" : rest_id}
    else:
        result =  {"success" : False,
                    "message" : "Si è verificato un problema nel salvataggio del ristorante %s" % rest_id ,
                    "restaurant_id" : rest_id}
    return  jsonify(result)


def deleteUnusedUploadedFiles():
    pass
    
