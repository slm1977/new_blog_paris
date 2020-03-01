
import os

from project.restaurants_reader import readRestaurants

flask_ip="192.168.0.118:5000"
#flask_ip="127.0.0.1:5000"

def generate_quartiere(quartiere, pages):
    print("Creazione pagine %s per quartiere %s" , (pages, quartiere))
    for p in pages:
        #html_filename = "pagesToConvert/pagina%s.html" % p
        html_filename = "http://%s/ristoranti/%s/%s/" % (flask_ip, quartiere,p)
        #png_filename = "convertedPages/pagina%s.png" % p
        png_filename = "static/pages/%s_pagina_%s.png" % (quartiere, p)
        cmd = "google-chrome --headless --screenshot --window-size=450,550 --default-background-color=0 %s" % html_filename
        print(cmd)
        os.system(cmd)
        print("renaming screenshot.png -> %s" % png_filename)
        os.rename(r'screenshot.png',r'%s' % png_filename)

    print("done")


ristoranti = readRestaurants()
quartieri = list(ristoranti.keys())
print("quartieri:%s" % quartieri )
for q in quartieri:
    if not q:
        continue
    print("Quartiere:%s" % ristoranti[q])
    pages = range(2*len(ristoranti[q])+1)
    print("Creo pagine per %s" % q)
    generate_quartiere(q,pages)

