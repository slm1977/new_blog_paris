
from flask import Flask, flash, send_from_directory, current_app,  Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os


from  project.ristoranti import ristoranti
#from .itinerari import itinerari
#from .testi import pagine

from .db_queries import get_pages, add_zone_to_db, add_restaurant_to_db
#from .models import Restaurant,Zone

main = Blueprint('main', __name__,template_folder='templates',static_folder='static')

#https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
#https://stackoverflow.com/questions/54733662/how-to-send-html-data-to-flask-without-form
#https://stackoverflow.com/questions/24577349/flask-download-a-file


# MESSENGER CHAT PLUGIN
#https://developers.facebook.com/docs/messenger-platform/discovery/customer-chat-plugin#steps


"""
@main.route("/itinerari/<int:indice>/")
def caricaItinerario(indice):
    return render_template("blog_itinerario.html", itinerario=itinerari[indice])



@main.route("/itinerari/")
def mostraItinerari():
    return render_template("blog_itinerari.html", itinerari=itinerari)
"""

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



@main.route("/")
def home():
    menu= get_pages()
    page_id = menu[0].id
    return redirect("/load_page/%s" % page_id)





@main.route("/inner_book/<quartiere>/")
def caricaLibroRistorante(quartiere):
    return render_template("blog_restaurant.html", quartiere=quartiere,menu=get_pages(), page_id=-2)

@main.route("/ristoranti/")
def mostra_ristoranti():
    # (900,550) dimensione del book al 100%
    ord_ristoranti = list(ristoranti.keys())
    ord_ristoranti.sort()
    return render_template("blog_restaurants.html", ristoranti= ord_ristoranti, menu=get_pages(), page_id=-2)
    #return book("marais")



@main.route("/book/<quartiere>/")
def book(quartiere):
    print("In book:%s" % quartiere);
    myvideo = url_for("static", filename="fotoblog/ristoranti/levieuxbelleville.mp4")
    return render_template("book2.html", ristoranti=ristoranti[quartiere], countRest=len(ristoranti[quartiere]),
                           quartiere=quartiere, myvideo=myvideo)


@main.route("/ristoranti/<quartiere>/<int:n>/")
def restaurants(quartiere,n):
    r = ristoranti[quartiere]
    print("Ristoranti del %s\n\n" % quartiere)
    if (n==0):
        return render_template('rest_page_front_title.html', rist=r[0])

    #elif (n==len(r)-1 and n%2==1):
    #    return render_template('rest_page_back.html', rist=r[n-1])

    elif (n%2==1):
        return render_template('rest_page_left.html', rist=r[int((n - 1) / 2)])
    else:
        return render_template('rest_page_right_images.html', rist=r[int((n-2) / 2)])



@main.route("/collage/")
def collage():
    return redirect(url_for("static", filename="collage/index.html"))



@main.route("/video/<quartiere>/<int:n>/")
def video(quartiere,n):
    r = ristoranti[quartiere]
    myvideo = url_for("static", filename="fotoblog/ristoranti/levieuxbelleville.mp4")
    return render_template('rest_page_right.html', rist=r[n], myvideo=myvideo)


 
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
    print("RICHIAMATO UPLOAD")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return url_for('main.uploaded_file',
                                    filename=filename)
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

