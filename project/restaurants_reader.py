import xlrd
import os
from os import path
import pygame

"""
"titolo": "Flam's",
"indirizzo": "62 rue des Lombards",
"orari": "dom-gio:11:45 - 23:30 ven-sab:11:45 - 00:00,prenotazione via web",
"quartiere": "Marais",
"caratteristiche": "pizza alsaziana menu fisso 15euro",
"descrizione": "da non perdere!",
"""

def getImageSize(filepath):
    img = pygame.image.load(filepath)
    width = img.get_width()
    height = img.get_height()
    return (width>=height, width,height)


def getImages(titolo_ristorante):
    web_dir = "fotoblog/ristoranti/%s" % titolo_ristorante.lower().strip().replace(" ", "_").strip()
    dir = "static/%s" % web_dir
    print("dir:%s" % dir)
    if not path.isdir(dir):
        return []

    images = []

    for f in os.listdir(dir):
        filename = "%s/%s" % (dir,f)
        try:
            image_size = getImageSize(filename)
            images.append( ("%s/%s" % (web_dir, f) , image_size) )
        except Exception:
            continue

    return images
    #return ["%s/%s" % (web_dir, fn) for fn in  os.listdir(dir)]




def readRestaurants():
    ristoranti = {}

    loc = "ristoranti2.xlsx"

    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    # For row 0 and column 0
    print(sheet.cell_value(0, 0))
    print("Numero righe:%s" % sheet.nrows)

    for r in range(1,sheet.nrows):
        quartiere = sheet.cell_value(r, 0).capitalize()
        qkey = quartiere.lower().replace(" ", "")
        print(quartiere)
        if not qkey:
            continue
        if not qkey in ristoranti:
            ristoranti[qkey]=[]
        titolo = sheet.cell_value(r, 1).capitalize().strip()
        indirizzo = sheet.cell_value(r, 2)
        caratteristiche = sheet.cell_value(r, 3).capitalize()
        descrizione = sheet.cell_value(r, 4).capitalize()
        orari = sheet.cell_value(r, 5)
        images = getImages(titolo)



        ristoranti[qkey].append({
            "titolo": titolo,
            "indirizzo": indirizzo,
            "orari": orari,
            "quartiere": quartiere,
            "caratteristiche": caratteristiche,
            "descrizione": descrizione,
            "immagini" : images
        })

    print("ristoranti=%s" % ristoranti)

    print("aggiorno il file dei ristoranti")
    f = open("ristoranti.py", "w")
    f.write("ristoranti=%s" % ristoranti)
    f.close()
    print("File aggiornato")

    return ristoranti


ristoranti = readRestaurants()


if __name__== "__main__":
    print("percorso:")

    print(os.getcwd())
    print (getImages("La crete"))






