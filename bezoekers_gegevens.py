import tkinter
import re
import csv
from PIL import ImageTk, Image
import qrcode
from qrcode.image.pure import PymagingImage
from tkinter.messagebox import showerror
import uuid


def gegevens_vragen(titel, starttijd, aanbieder):
    """
    In deze functie worden alle gegevens gevraagd m.b.t de bezoeker.
    De voornaam, achternaam en e-mail adres worden hier gevraagd en opgeslagen in 'label' variabele
    zodat deze later kunnen gebruikt worden om weer te geven.
    """

    def gegevens_doorsturen():
        controle_gegevens(invoer_voornaam.get(), invoer_achternaam.get(), invoer_email.get(), titel_film, starttijd_film
                          , aanbieder_film)
        vernietig_scherm()

    def vernietig_scherm():
        root.destroy()

        
    titel_film = titel
    starttijd_film = starttijd
    aanbieder_film = aanbieder

    root = tkinter.Tk()
    root.geometry('{}x{}'.format(400, 250))
    root.title("Gegevens invoeren")

    label_voornaam = tkinter.Label(root, text="Wat is uw voornaam?")
    label_achternaam = tkinter.Label(root, text="Wat is uw achternaam?")
    label_emailadres = tkinter.Label(root, text="Wat is uw e-mailadres?")
    invoer_voornaam = tkinter.Entry(root)
    invoer_achternaam = tkinter.Entry(root)
    invoer_email = tkinter.Entry(root)
    reserveren_button = tkinter.Button(root, text="Reserveren", command=gegevens_doorsturen)


    label_voornaam.pack()
    invoer_voornaam.pack()
    label_achternaam.pack()
    invoer_achternaam.pack()
    label_emailadres.pack()
    invoer_email.pack()
    reserveren_button.pack()

    root.mainloop()


def controle_gegevens(voornaam, achternaam, email, titel, starttijd, aanbieder):
    """
    In deze functie worden alle gegevens, die ingevoerd worden door de bezoeker,
    gecheckt of deze daadwerkelijk kloppen. Dit wordt gedaan door te checken of de naam
    alleen maar alphanumerieke tekens er in heeft. Daarna wordt gekeken of het e-mail syntactisch correct is.
    Als een van deze 'checks' falen, dan krijgen ze een foutmelding. Als de gegevens wel kloppen, voer dan
    code_genereren() uit.
    """
    if voornaam.isalpha() and achternaam.isalpha():
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            code_genereren(voornaam, achternaam, email, titel, starttijd, aanbieder)

        else:
            showerror(title= "Verkeerde email", message="Volgens mij heeft u een verkeerd e-mail ingevoerd, probeer opnieuw.")
            gegevens_vragen(titel, starttijd, aanbieder)
    else:
        showerror(title="Leestekenfout", message="Uw voornaam of achternaam heeft leestekens en/of cijfers, probeer het opnieuw.")
        gegevens_vragen(titel, starttijd, aanbieder)


def code_genereren(voornaam, achternaam, email, titel, starttijd, aanbieder):
    """
    Deze functie krijgt gegevens mee uit controle_gegevens(). De (gecontroleerde) gegevens bestaat uit een voornaam,
    achternaam en e-mail adres van de bezoeker. Deze functie zal een code genereren op basis van de library 'uuid'
    die willekeurige codes kan genereren.
    """
    code = uuid.uuid4()
    qr_code_maken(voornaam, achternaam, titel, starttijd, code)
    gegevens_opslaan(voornaam, achternaam, email, titel, starttijd, aanbieder, code)


def gegevens_opslaan(voornaam, achternaam, email, titel, starttijd, aanbieder, code):
    """
    Deze functie krijgt gegevens mee uit controle_gegevens(). De (gecontroleerde) gegevens bestaat uit een voornaam,
    achternaam en e-mail adres van de bezoeker. Deze functie zal deze gegevens opslaan in een .csv bestand volgens
    de volgende tabel:

    Filmkauze, tijdskeuze, unieke code, voornaam, achternaam, e-mail adres.

    Deze worden opgeslagen in bezoeker_gegevens.csv
    """
    with open("bezoeker_gegevens.csv", "a") as bezoeker_gegevens_bestand:
        bezoekerbestand = csv.writer(bezoeker_gegevens_bestand)
        bezoekerbestand.writerow([aanbieder, starttijd, titel, voornaam, achternaam, email, code])
    bezoeker_gegevens_bestand.close()


def qr_code_maken(voornaam, achternaam, titel, starttijd, code):
    """
    In deze functie wordt een QR-code gegenereerd, op basis van de code die gegeven wordt door code_generen().
    Nadat de QR-code gegenereerd is, zal deze worden opgeslagen in een .png file met de unieke code als titel.
    """
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4,)
    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image(image_factory=PymagingImage)

    with open('%s.png' % code, 'wb') as f:
        img.save(f)

    gegevens_weergeven(voornaam, achternaam, titel, starttijd, code)


def gegevens_weergeven(voornaam, achternaam, titel, starttijd, code):
    """
    In deze functie zullen alle gegevens, die boven gegenereerd en meegestuurd zijn, weergegeven worden. Dit wordt
    gedaan d.m.v een tkinter scherm die.
    """
    root = tkinter.Tk()
    root.geometry('{}x{}'.format(400,250))
    root.title("Uw gegevens")

    label_gegevens = tkinter.Label(root, text="U heeft gereserveerd onder de naam:")
    label_print_gegevens = tkinter.Label(root, text= voornaam +" "+ achternaam)
    label_filminfo = tkinter.Label(root, text="Voor de film:")
    label_print_filminfo = tkinter.Label(root, text= titel +" om "+ starttijd)
    label_code = tkinter.Label(root, text= "Uw unieke code, houd deze goed bij u!")
    button_ok = tkinter.Button(root, text= "OK", command=root.destroy)
    label_print_code = tkinter.Label(root, text= code)

    label_gegevens.pack()
    label_print_gegevens.pack()
    label_filminfo.pack()
    label_print_filminfo.pack()
    label_code.pack()
    label_print_code.pack()
    button_ok.pack(side=tkinter.BOTTOM)



    root.mainloop()
    qr_code_weergeven(code)


def qr_code_weergeven(code):
    """
    Helaas werkt deze functie niet.
    Deze functie zal de QR-code weergeven in een venster.
    """
    pass

