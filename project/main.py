from flask import Flask, flash, session, abort, send_from_directory, current_app,  Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from project.db_queries import get_zone, get_zones, get_restaurants_by_zone
import os


from  project.ristoranti import ristoranti
#from .itinerari import itinerari
#from .testi import pagine

from .db_queries import get_pages, add_zone_to_db, add_restaurant_to_db
#from .models import Restaurant,Zone

main = Blueprint('main', __name__,template_folder='templates',static_folder='static')

# sessions in FLASK
#https://pythonbasics.org/flask-sessions/

#https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
#https://stackoverflow.com/questions/54733662/how-to-send-html-data-to-flask-without-form
#https://stackoverflow.com/questions/24577349/flask-download-a-file


# MESSENGER CHAT PLUGIN
#https://developers.facebook.com/docs/messenger-platform/discovery/customer-chat-plugin#steps


@main.route("/")
def home():
    menu= get_pages()
    page_id = menu[0].id
    return redirect("/load_page/%s" % page_id)

@main.route("/offerte/")
def offerte():
    return render_template("offerte.html",  menu=get_pages(), page_id=-2, minicontent=True)

@main.route("/ristoranti/")
def mostra_ristoranti():
    # rimuovo le variabili di sessione relative al ristorante
    unset_active_restaurant()
    ord_quartieri = get_zones()
    print("QUARTIERI:%s" % ord_quartieri)
    return render_template("new_blog_restaurants.html", quartieri= ord_quartieri, menu=get_pages(), page_id=-2)
    

@main.route("/inner_book2/<zone_id>/")
def caricaLibroRistorante2(zone_id):
    session['active_zone_id'] = zone_id
    return render_template("new_blog_restaurant.html", zone_id=zone_id,menu=get_pages(), page_id=-3)


@main.route("/book2/<int:zone_id>/")
def book2(zone_id):
    print("In book:%s" % zone_id)
    quartiere = get_zone(zone_id)
    if quartiere==None:
        abort(404)
    print("ZONA: %s" % quartiere.name)
    r = get_restaurants_by_zone(zone_id)
    return render_template("new_book2.html", ristoranti=r, countRest=len(r),
                           quartiere=quartiere)

@main.route("/ristoranti2/indice/<int:zone_id>/")
def zone_restaurants_index(zone_id):
    quartiere = get_zone(zone_id)
    zone = get_zone(zone_id)
    if quartiere==None:
        abort(404)
    rist = get_restaurants_by_zone(zone_id)
    rist_info = []
    for r in rist:
        rist_info.append({"id": r.id, "name":r.name, 
        "lat" : r.latitude, "lon" : r.longitude})
    return render_template("index_of_contents_restaurants_left.html",  countRest = len(rist), rist=r, quartiere=zone)
    
    #return render_template("index_of_contents_restaurants_right.html",  countRest = len(rist), rist=rist_info, quartiere=zone)

@main.route("/ristoranti2/<int:zone_id>/<int:n>/")
def restaurants2(zone_id,n):
    quartiere = get_zone(zone_id)
    if quartiere==None:
        abort(404)
    print("ZONA: %s" % quartiere.name)
    rist = get_restaurants_by_zone(zone_id)
    zone = get_zone(zone_id)
    print("Ristoranti del %s\n\n" % rist)
    if (n==0):
        return render_template('new_base_restaurants_front_title2.html', quartiere=quartiere.name)
    elif (n==1):
        return render_template("index_of_contents_restaurants_left.html",  
        countRest = len(rist), rist=rist, quartiere=zone)
    elif (n==2):
        rist_info = []
        for r in rist:
            rist_info.append({"id": r.id, "name":r.name, 
        "lat" : r.latitude, "lon" : r.longitude})
        return render_template("index_of_contents_restaurants_right.html",  countRest = len(rist), rist=rist_info, quartiere=zone)
    elif (n%2==1):
        return render_template('new_rest_page_left.html', rist=rist[int((n - 3) / 2)])
    else:
        return render_template('new_rest_page_right_images.html', rist=rist[int((n-4) / 2)])


@main.route('/edit_active_restaurant/', methods=['GET'])
@login_required
def edit_active_restaurant():
    restaurant_id = session['active_restaurant_id'] 
    if restaurant_id==None or restaurant_id<1:
        return redirect(request.referrer)

    #zone_id = session['active_zone_id'] 
    return redirect("/restaurant/edit/%s/" % restaurant_id)

@main.route('/set_active_restaurant/', methods=['POST'])
@login_required
def set_active_restaurant():
    zone_id = request.form.get('zone_id', None)
    page_index = request.form.get('page_index', None)
    r = get_restaurants_by_zone(zone_id)
    r_index = int(page_index)//2-2
    restaurant_id = None if (r_index<0 or r_index>=len(r)) else r[r_index].id
    session['active_restaurant_id'] = restaurant_id
    session['active_zone_id'] = zone_id
    session['active_page_index'] = page_index if page_index!=None else 1
    print("salvata variabile di sessione zona:%s ristorante:%s" % (session['active_zone_id'],
                                                                   session['active_restaurant_id']))
    return jsonify({"success" : True})

@main.route('/unset_active_restaurant/', methods=['POST'])
@login_required
def unset_active_restaurant():
    session['active_restaurant_id'] = 0
    session['active_zone_id'] = 0
    session['active_page_index'] = 1 
    """
    session.pop('active_restaurant_id', None)
    session.pop('active_zone_id', None)
    session.pop('active_page_index', None)
    """
    return jsonify({"success" : True})


#
# FILE UPLOAD CODE
#
#https://stackoverflow.com/questions/44926465/upload-image-in-flask
#https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     

@main.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload_file():
    print("RICHIAMATO UPLOAD con method:%s" % request.method)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print("NO FILE PART")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            print("NO SELECTED FILE")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            prefix = request.form.get('prefix',"")
            print("Prefisso filename:%s" % prefix)
            db_filename = "%s%s" % (prefix,filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], db_filename))
            print("IMMAGINE SALVATA CON SUCCESSO")
            return url_for('main.uploaded_file',
                                    filename=db_filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)



"""
@main.route("/itinerari/<int:indice>/")
def caricaItinerario(indice):
    return render_template("blog_itinerario.html", itinerario=itinerari[indice])



@main.route("/itinerari/")
def mostraItinerari():
    return render_template("blog_itinerari.html", itinerari=itinerari)


@main.route("/insert_rest/")
@login_required
def insertRestaurants():
    quartieri = ristoranti.keys()
    q_id= 14 # id del quartiere latino
    for q in quartieri:
        for r in ristoranti[q]:
            quartiere = r["quartiere"]
            name = r["titolo"]
            address = r["indirizzo"]
            topic = r["caratteristiche"]
            description = r["descrizione"]
            zone_id = q_id
            orari = r["orari"]
            index = 1
            print("%s: id:%s Rist:%s" % (quartiere, q_id, name))
            add_restaurant_to_db(name=name, address=address, topic=topic,
                                 description=description, zone_id=zone_id,
                                 index=index, orari=orari)
        q_id +=1

    return "Ok"
"""


