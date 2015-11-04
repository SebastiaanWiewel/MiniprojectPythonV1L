__author__ = 'Sebastiaan'
import tkinter
import csv
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

"""
In deze functie word het aanbieder menu weergegeven. Deze word doorverwezen vanuit het hoofdscherm met een knop.
In het menu vind je 2 knoppen terug.
1. Een code checken vanuit bezoeker_gegevens.csv om te kijken of een gebruiker een geldige code heeft.
2. Een button om een lijst te printen welke gebruikers kijken of komen kijken naar de film(s). Hierbij word er geprint met de volgorde: Filmtitel, Starttijd, Achternaam, Voornaam, E-mailadres.
"""

def aanbieder_inloggen():
    """
    In deze functie logt de gebruiker in.
    :param aanbieder_gebruikersnaam
    :param aanbieder_wachtwoord
    :param aanbieder_email
    """

    root = tkinter.Tk()
    # Maakt venter in pixel grootte
    root.geometry('{}x{}'.format(400, 250))
    root.title("Inlog menu")

    # Maakt labels voor informatie
    label_gebruikersnaam = tkinter.Label(root, text="Voer uw gebruikersnaam in:")
    label_wachtwoord = tkinter.Label(root, text="Voer uw wachtwoord in:")

    # Maakt een vak aan waar informatie ingevuld kan worden
    aanbieder_gebruikersnaam = tkinter.Entry(root)
    aanbieder_wachtwoord = tkinter.Entry(root)

    # Maakt een button
    inloggen_button = tkinter.Button(root, text="Inloggen", command=lambda: vergelijken_invoer(aanbieder_gebruikersnaam.get(), aanbieder_wachtwoord.get()))

    # Pakt alles in
    label_gebruikersnaam.pack()
    aanbieder_gebruikersnaam.pack()
    label_wachtwoord.pack()
    aanbieder_wachtwoord.pack()
    inloggen_button.pack()

    def vergelijken_invoer(aanbieder_gebruikersnaam, aanbieder_wachtwoord):
        """
        Deze functie controleert of de gebruikersnaam en wachtwoord gelijk zijn aan wat er in de database staat. En opent het menu.
        :param aanbieder_gebruikersnaam:
        :param aanbieder_wachtwoord:
        """
        try:
            file_open = open("aanbieder_login.csv", "r")
            reader = csv.DictReader(file_open, delimiter=";")
            for row in reader:
                if aanbieder_gebruikersnaam == row["gebruikersnaam"] and aanbieder_wachtwoord == row["wachtwoord"]:
                    root.destroy()
                    aanbieder_menuscherm(aanbieder_gebruikersnaam)
                    break
                else:
                    continue
            else:
                showerror(title="Verkeerde inlogpoging", message="De invoer is onjuist, probeer opnieuw.")
        finally:
            file_open.close()

    root.mainloop()


def aanbieder_menuscherm(aanbieder_gebruikersnaam):
    root = tkinter.Tk()
    root.geometry('{}x{}'.format(500, 250))
    root.title("Aanbieder menu")

    # Krijgt mee van Sebastiaan wie de aanbieder is
    # Aanbieder moet de ticket-code intypen
    # Programma controleert of deze code overeen komt met de aanbieder.

    label_welkomsbericht = tkinter.Label(root, text="Welkom in het aanbiedersscherm, welke actie wilt u uitvoeren?")
    label_check_code = tkinter.Label(root, text="Check deze code:")
    code_invoer = tkinter.Entry(root)
    code_checken = tkinter.Button(root, text="Controleer code", command=lambda: code_controle(code_invoer.get()))
    #label_filmlijst = tkinter.Label(root, text= "Weten wie gaat kijken?")
    filmlijst_display = tkinter.Button(root, text="Reserveringslijst", command=lambda: aanbieder_filmlijst(aanbieder_gebruikersnaam))
    terug_naar_venster = tkinter.Button(root, text="Terug naar hoofdscherm", command=root.destroy)

    label_welkomsbericht.pack()
    label_check_code.place(x=10, y=30)
    code_invoer.place(x=10, y=60, width=300, height=25)
    code_checken.place(x=10, y=90, width=120, height=25)
    terug_naar_venster.place(x=300, y=90, width=150, height=25)
    #label_filmlijst.place(x = 10, y = 140)
    filmlijst_display.place(x=10, y=170, width=120, height=25)

    def code_controle(code_invoer):
        """
        Deze functie kijkt naar de invoer van de ingelogde aanbieder die een code controlleerd van een bezoeker.
        :param code_invoer:
        """
        aanbieder = aanbieder_gebruikersnaam
        try:
            file_open = open("bezoeker_gegevens.csv", "r")
            reader = csv.DictReader(file_open, delimiter=",")
            for row in reader:
                if str(code_invoer) == row['Code'] and aanbieder in row['Aanbieder']:               #code controle gelijk aan invoer code en in een lijn van de aanbieder
                    showinfo(title="Gecheckte code", message= "\nBijbehorende gegevens:\nNaam:  " + #printen van gegevens
                                                              row['Voornaam']+ "\n Achternaam: " +
                                                              row['Achternaam']+ "\n E-mail: " +
                                                              row['Email'])
                    break
                else:
                    continue
            else:
                showerror(title="Verkeerde code", message="De invoer is onjuist, probeer opnieuw.")
        finally:
            file_open.close()
    root.mainloop()


def aanbieder_filmlijst(aanbieder_gebruikersnaam):
    """
    Deze functie geeft weer welke gebruikers op dit moment op de lijst staan van reserveringen.
    :param aanbieder_gebruikersnaam:
    """
    filmkijker_lijst = []
    root = tkinter.Tk()
    root.geometry('{}x{}+{}+{}'.format(1000,250,200,200))
    root.title("Deze personen staan op de lijst")
    try:
        file_open = open("bezoeker_gegevens.csv", "r")
        reader = csv.DictReader(file_open, delimiter=",")
        grid = 0
        for row in reader:
            if aanbieder_gebruikersnaam in row['Aanbieder']:
                grid += 1
                label = tkinter.Label(root, text="(" + row['Titel']+"  " + row['Starttijd'] + ')'+"  "+ row['Achternaam']+ ', '+ row['Voornaam']+ ' -- '+
                                                 row['Email'] + ' -- ' + row['Code'])
                label.pack(side=tkinter.TOP)
    finally:
        file_open.close()

    root.mainloop()
    print(filmkijker_lijst)


