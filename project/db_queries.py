from project import db
from project.models import Page, Restaurant, Zone
from flask import url_for

import logging
import time

LOG = logging.getLogger(__name__)


class MenuTypes:
    PAGE = 0
    RESTAURANT = 1

def get_pages():
    pages = Page.query.filter_by(deleted=False).order_by(Page.index).all()
    return pages

def get_zones(order=Zone.index):
    zones = Zone.query.filter_by(deleted=False).order_by(order).all()
    return zones

def get_zone(zone_id):
    zone = Zone.query.filter_by(deleted=False, id=zone_id).first()
    print("zona da db:%s" % zone)
    return zone

def update_zones(zones, zones_id):
    LOG.info("ZONE DA AGGIORNARE:%s" % zones_id)
    index = 1
    for zone_id in zones_id:
        try:
            new_zone_dict = zones[zone_id]
            LOG.info("AGGIORNO ZONA")
            LOG.info(new_zone_dict)
            zone = Zone.query.filter_by(id=int(zone_id)).first()
            zone.name = new_zone_dict["name"]
            zone.visible = bool(new_zone_dict["visible"])
            zone.deleted = bool(new_zone_dict["deleted"])

            if zone.deleted:
                zone.name = "%s_deleted_%s" % (zone.name, int(time.time()))

            zone.index = index
            db.session.commit()
            index +=1
        except Exception as ex:
            LOG.error("Eccezione nell'aggiornamento del quartiere sul db:%s" % ex)
            db.session.rollback()
            result = {"success": False, "message": "Eccezione nell'aggiornamento delle zone sul db:%s" % ex}
            return result

    result = {"success": True, "message": "Zone aggiornate con successo!!"}
    return result

def get_last_created_page():
    return Page.query.order_by(Page.id.desc()).first()

def add_zone_to_db(zone_title, index=1):
    try:
        new_zone = Zone(name=zone_title, index=index, visible=False, deleted=False)
        db.session.add(new_zone)
        db.session.commit()
    except Exception as ex:
        LOG.error("Eccezione nella scrittura del quartiere sul db:%s" % ex)
        result = {"success": False, "message": "Zona non aggiunta: %s" % ex}
        return result
    result = {"success": True, "message": "Zona aggiunta con successo"}

    return result

def get_restaurants_by_zone(zone_id, visible=None):
    if visible==None:
        return Restaurant.query.filter_by(deleted=False, zone_id=zone_id).order_by(Restaurant.id).all()
    else:
        return Restaurant.query.filter_by(deleted=False, zone_id=zone_id, visible=bool(visible)).order_by(Restaurant.id).all()

def get_next_restaurant_id():
    last_id = Restaurant.query.order_by(Restaurant.id.desc()).first().id
    return last_id+1

def get_next_page_id():
    last_id = Page.query.order_by(Page.id.desc()).first().id
    return last_id+1

def add_restaurant_to_db(rest_id, name, address, topic, description, zone_id, orari, 
visible, latitude, longitude, images, index=1):
    try:
        new_restaurant = Restaurant(name=name, address=address, 
                topic=topic, description=description, zone_id=zone_id, 
                orari=orari, visible=visible, latitude=latitude, longitude=longitude, 
                images=images, index=index)

        LOG.info("Aggiunta su db del ristorante %s" % name )
        db.session.add(new_restaurant)
        db.session.commit()
    except Exception as ex:
        print("Eccezione nella scrittura del ristorante sul db:%s" % ex)
        #raise ex
        return None
    return None


def update_restaurant(rest_id, name, address, topic, description, zone_id, orari, 
visible, latitude, longitude, images, index=1):

    try:
        rest = Restaurant.query.get(rest_id)
        if rest==None:
            return add_restaurant_to_db(rest_id, name, address, topic, description, zone_id, orari, 
visible, latitude, longitude, images, index=1)

        rest.name = name
        rest.address = address
        rest.topic = topic
        rest.description = description
        rest.zone_id = zone_id
        rest.orari = orari
        rest.latitude = latitude
        rest.longitude = longitude
        rest.visible = bool(visible)
        rest.deleted = bool(False)
        rest.images = images
        rest.index = index
        db.session.commit()
        return rest_id
    except Exception as ex:
        LOG.error("Eccezione nell'aggiornamento del ristorante %s sul db:%s" % (rest_id,ex))
        #raise ex
        return None


def add_page_to_db(menu_title, visible, index=None):
    try:
        # create new page with the form data. Hash the password so plaintext version isn't saved.
        last_id = Page.query.order_by(Page.id.desc()).first().id
        if index == None:
            index = last_id
        filename= "page_%s.html" % (last_id+1)
        #path = "./project/static/menu_pages/%s" % filename
        path = ".%s" % url_for("static", filename="menu_pages/%s" % filename)
        new_page = Page(menu_title=menu_title,path=path, index=int(index), 
        visible=bool(visible),deleted=bool(False), type=MenuTypes.PAGE)

        # add the new page to the database
        db.session.add(new_page)
        db.session.commit()
        return Page.query.order_by(Page.id.desc()).first()

    except Exception as ex:
        LOG.error("Eccezione nella scrittura della pagina sul db:%s" % ex)
        #raise ex
        return None

    return None

def update_page(page_id, new_menu_title, visible):

    try:
        page = Page.query.get(page_id)
        page.menu_title = new_menu_title
        page.visible = bool(visible)
        db.session.commit()
        return page.path
    except Exception as ex:
        LOG.error("Eccezione nell'aggiornamento della pagina sul db:%s" % ex)
        #raise ex
        return None



def update_pages_index(id_list):
    try:
        id_list = id_list.split(",")
        LOG.info("Lista degli id ordinati:%s" % id_list)
        for i in range(len(id_list)):
            page = Page.query.get(int(id_list[i]))
            if page:
                page.index = (i+1)
                db.session.commit()
            else:
                print("Pagina con id:%s non trovata nella lista" % id_list[i] )
        result = {"success": True, "message": "Ordine delle pagine aggiornato"}
        return result
    except Exception as ex:
        LOG.error("Eccezione salvataggio ordinamento:%s" % ex)
        db.session.rollback()
        result =  {"success": False, "message": "Eccezione salvataggio ordinamento:%s" % ex}
        return result


def delete_page(page_id):
    page = Page.query.filter_by(id=page_id).first()
    if page==None:
        return None
    filepath = page.path
    LOG.info("Sto rimuovendo la pagina con id:%s" % page.id)
    #db.session.query(Page).filter(Page.id == page.id).delete(synchronize_session=False)
    page.deleted = True
    db.session.commit()
    LOG.info("Pagina rimossa (contrassegnata come DELETED")
    return filepath

def delete_restaurant(restaurant_id):
    rest = Restaurant.query.filter_by(id=restaurant_id).first()
    if rest==None:
        return None
    rest.deleted = True
    db.session.commit()
    LOG.info("Ristorante rimosso (contrassegnato come DELETED")
    return restaurant_id



    filepath = page.path
    LOG.info("Sto rimuovendo il ristorantae con id:%s" % page.id)
    db.session.query(Page).filter(Page.id == page.id).delete(synchronize_session=False)
    db.session.commit()
    LOG.info("Pagina rimossa")
    return restaurant_id











