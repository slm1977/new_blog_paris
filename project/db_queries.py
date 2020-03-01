from project import db
from models import Page
from flask import url_for

import logging
LOG = logging.getLogger(__name__)

def get_pages():
    pages = Page.query.order_by(Page.index).all()
    return pages

def get_last_created_page():
    return Page.query.order_by(Page.id.desc()).first()

def add_page_to_db(menu_title, visible, index=None):
    try:
        # create new page with the form data. Hash the password so plaintext version isn't saved.
        last_id = Page.query.order_by(Page.id.desc()).first().id
        if index == None:
            index = last_id
        filename= "page_%s.html" % (last_id+1)
        #path = "./project/static/menu_pages/%s" % filename
        path = ".%s" % url_for("static", filename="menu_pages/%s" % filename)
        new_page = Page(menu_title=menu_title,path=path, index=int(index), visible=bool(visible))

        # add the new page to the database
        db.session.add(new_page)
        db.session.commit()
        return Page.query.order_by(Page.id.desc()).first()

    except Exception as ex:
        print("Eccezione nella scrittura della pagina sul db:%s" % ex)
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
        print("Eccezione nell'aggiornamento della pagina sul db:%s" % ex)
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
        print("Eccezione salvataggio ordinamento:%s" % ex)
        db.session.rollback()
        result =  {"success": False, "message": "Eccezione salvataggio ordinamento:%s" % ex}
        return result


def delete_page(page_id):
    page = Page.query.filter_by(id=page_id).first()
    if page==None:
        return None
    filepath = page.path
    print("Sto rimuovendo la pagina con id:%s" % page.id)
    db.session.query(Page).filter(Page.id == page.id).delete(synchronize_session=False)
    db.session.commit()
    print("Pagina rimossa")
    return filepath









