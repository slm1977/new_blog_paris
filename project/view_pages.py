import logging
import os
import time

from flask import Flask, current_app,  Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user

from .models import Page
from . import db
from .db_queries import get_pages, add_page_to_db, update_page, delete_page, update_pages_index, get_last_created_page


LOG = logging.getLogger(__name__)

pages = Blueprint('pages', __name__,template_folder='templates',static_folder='static')

@pages.route("/create/")
@login_required
def create_new_page():
    return page_edit()


@pages.route("/load_last_page/")
@login_required
def load_last_created_page():
    print("Richiamata load_last_page")
    last_id = Page.query.order_by(Page.id.desc()).first().id
    return load_page(last_id)


@pages.route("/load_menu_page/<menu_page_index>/")
def load_menu_page(menu_page_index):
    try:
        page = get_pages()[int(menu_page_index)]
        print("Trovata pagina:%s" % page)
        if page==None:
            raise Exception("Impossibile trovare la pagina di menu n.%s" % menu_page_index)
        return load_page(page.id)
    except Exception as ex:
        print ("load_menu_page Exception:%s" % ex)
        return redirect("/")

@pages.route("/load_page/<page_id>/")
def load_page(page_id):
    page = Page.query.filter_by(id=page_id).first()
    if (not page.visible and not current_user.is_authenticated):
        return redirect("/login")

    LOG.info('Carico la pagina dal percorso:%s', page.path)
    LOG.info('directory corrente:%s',os.getcwd())
    LOG.info('app_root_path:%s', current_app.root_path)

    filepath= os.path.join(current_app.root_path,page.path)
    f = open(filepath, "r")
    content = f.read()
    f.close()
    pagina = {"contenuto" : content}
    return render_template("blog_content.html", pagina=pagina, menu=get_pages(), page_id=page_id)


@pages.route("/sort_pages/", methods=["GET", "POST"])
@login_required
def sort_pages():
    if request.method=="GET":
        pages_id = []
        pages = get_pages()
        for p in pages:
            pages_id.append(p.id)
        return render_template("page_sorting.html", pages=pages, pages_id=pages_id)
    else:
        pages_id = request.form['pages_id']
        print("ID PAGINE DA AGGIORNARE:")
        print(pages_id)
        result = update_pages_index(pages_id)
        return jsonify(result)



@pages.route("/edit/<page_id>/")
@login_required
def page_edit(page_id=None):
    #send_from_directory("static", 'itinerari/itinerario_01.html')
    #print(url_for("static", filename="itinerari/itinerario_01.html"))
    if page_id!=None and int(page_id)<-1:
        print("pagina non editabile")
        return redirect("/")
    elif page_id==None or int(page_id)<0:
        return render_template("page_editor.html", content="", page=None)
    else:
        page = Page.query.filter_by(id=page_id).first()
        filepath = os.path.join(current_app.root_path, page.path)
        f = open(filepath, "r")
        content = f.read()
        f.close()
        return render_template("page_editor.html", content=content, page=page)


@pages.route("/save/", methods=["POST"])
@login_required
def save_page():
    form_data = request.form.get('content')
    menu_title = request.form.get('menu_title')
    page_id = request.form.get('id')
    visible = True if request.form.get('visible')=="true" else False
    print("Salvo con menu %s" % menu_title)
    print("Valore di visibilità %s" % visible)
    if page_id==None or int(page_id)<0:
        # crea una nuova pagina sul db e restituisce il path completo dove salvare il file
        newpage = add_page_to_db(menu_title=menu_title, visible=visible)
        if newpage!=None:
            page_id = newpage.id
            filenameToSave =  newpage.path
        else:
            page_id = -1
            filenameToSave = None

    else:
        # aggiorna la pagina preesistente
        filenameToSave = update_page(page_id,menu_title, visible)

    # il file viene creato solo se la pagina è stata aggiunta correttamente sul db
    if filenameToSave!=None:
        #print("Content:\n%s" % str(form_data))
        filepath = os.path.join(current_app.root_path, filenameToSave)
        print("Percorso di salvataggio:%s" % filepath)
        f = open(filepath, "w")
        f.write(form_data)
        f.close()
        result = {"success" : True,
                  "message" : "Pagina salvata (%s)" % filepath,
                  "page_id" : page_id}

        return jsonify(result)
    else:
        result = {"success": False,
                  "message": "Impossibile salvare la pagina. Verificare la unicità della voce di menu!",
                  "page_id" : -1}
        return jsonify(result)


@pages.route("/delete/<page_id>")
@login_required
def remove_page(page_id):
    print("RIMOZIONE PAGINA:%s" % page_id)
    # rimuovo la pagina dal db
    filepath = delete_page(page_id)
    if filepath!=None:
        abs_full_path = os.path.join(current_app.root_path, filepath)
        newfile_path = "%s_deleted_%s" % (abs_full_path, int(time.time()))
        os.rename(abs_full_path, newfile_path)
    return redirect("/")
