import io
from tkinter import *
from tkinter.messagebox import *
from urllib.request import urlopen
from PIL import ImageTk, Image
from aanbieder_menu import *
import datetime
import bezoekers_gegevens



__author__ = 'Jochem'

class LijstFrame(Frame):
    def __init__(self, parent, films):
        Frame.__init__(self, parent)
        self.parent = parent
        self.films = films
        self.infos = []
        self.initUI()

    def initUI(self):
        self.parent.title("Filmpje reserveren")
        self.parent.geometry('{}x{}+{}+{}'.format(1200, 950, 300, 0))

        self.index = 0

        #Maakt een knop waar de aanbieders mee kunnen inloggen
        self.button_aanbieder = Button(self, text="Aanbieder login", bg="red", fg="white", command=self.aanbieder_knop, padx=5, pady=3)
        self.button_aanbieder.pack(side=TOP)

        #Maakt een knop om naar de volgende pagina te gaan
        self.button3 = Button(self, text="Vorige",bg="blue", fg="white", command=self.vorige_knop, padx=5, pady=3)
        self.button3.pack(side=LEFT)

        #Maakt een knop om naar de vorige pagina te gaan
        self.button2 = Button(self, text="Volgende", bg="blue", fg="white", command=self.volgende_knop, padx=5, pady=3)
        self.button2.pack(side=RIGHT)
        self.scherm_tonen()


        self.pack()

    def volgende_knop(self):
        """
        Deze functie vernietigd eerst het oude scherm en maakt dan vervolgens weer een nieuw scherm aan met een hoger index zodat de volgende films
        getoond kunnen worden. In de if statement wordt er gekeken of de index niet groter wordt dat de totaal aantal films.
        """

        self.vernietig_scherm()
        if self.index <= (len(self.films)-3):   #Deze if statement kijkt wat de index van de film is en vergelijkt het met de lijst.
            self.index += 3                     #Als de index te hoog is dan zal hetzelfde scherm getoond worden,
            self.scherm_tonen()
        else:
            self.scherm_tonen()


    def vorige_knop(self):
        '''
        Deze functie vernietigd eerst het oude scherm en maakt dan vervolgens weer een nieuw scherm aan met een lager index zodat de volgende films
        getoond kunnen worden. In de if statement wordt er gekeken of de index niet kleiner wordt dat de totaal aantal films.
        '''
        self.vernietig_scherm()
        if self.index > 0:                     #Deze if statement kijkt wat de index van de film is en vergelijkt het met de lijst.
            self.index -= 3                    #Als de index te laag is dan zal hetzelfde scherm getoond blijven
            self.scherm_tonen()
        else:
            self.scherm_tonen()

    def aanbieder_knop(self):
        aanbieder_inloggen()

    def scherm_tonen(self):
        """
        Deze functie zorgt ervoor dat er drie films worden getoond op het scherm door middel van de index en door deze toe te voegen aan een lijst
        """
        self.infoscherm1 = FilmFrame(self,self.films[self.index])
        self.infos.append(self.infoscherm1)
        self.infoscherm2 = FilmFrame(self,self.films[self.index+1])
        self.infos.append(self.infoscherm2)
        self.infoscherm3 = FilmFrame(self,self.films[self.index+2])
        self.infos.append(self.infoscherm3)

    def vernietig_scherm(self):
        """
        Deze functie vernietigd de getoonde schermen
        """
        self.infoscherm1.destroy()
        self.infoscherm2.destroy()
        self.infoscherm3.destroy()





class FilmFrame(Frame):
    def __init__(self, parent, film):
        Frame.__init__(self, parent)

        self.parent = parent
        self.film = film
        self.initUI()

    def initUI(self):
        self.url_omzetten_naar_jpg()                                                        #Zet url om in een jpg bestand
        self.timestamp_omzetten_in_tijd()                                                   #Zet timestamp om in een tijd in 24 uur format
        self.splitten_van_genre()                                                           #Scheidt genre met"," ipv ":"

        self.text1 = Text(self, height=17, width= 21)                                       #Maakt een text window
        self.text1.insert(END, '\n')
        self.text1.image_create(END, image=(self.tk_image))                                 #Zet het jpg bestand in de window
        self.text1.pack(side=LEFT)                                                          #Plaatst de window aan de linker kant

        self.text2 = Text(self,height=15,width=150)                                         #Maakt een text window

        #Maakt een configuratie met namen om later naar te revereren
        self.text2.tag_configure('kopje', font=("Times New Roman", 12, "bold"))
        self.text2.tag_configure("informatie", font=("Calibri Light", 12))
        self.text2.tag_configure('groot', font=('Verdana', 20, 'bold'))

        #Stopt alle informatie van de films in de text window
        self.text2.insert(END,self.film["titel"], "groot")
        self.text2.insert(END, '\nJaar: ', 'kopje')
        self.text2.insert(END, self.film["jaar"], 'informatie')
        self.text2.insert(END, '\nRegisseur: ','kopje')
        try:                                                                                #Omdat van sommige films geen regisseur bekent is probeert deze try of er een regisseur is
            self.text2.insert(END, self.film["regisseur"], 'informatie')                    #Vervolgens plaats deze de regisseur in de tekst window
        except:                                                                             #Als er geen regisseur is dan wordt er "geen regisseur bekend" in de text window geplaatst
            self.text2.insert(END, "Regisseur niet bekend", "informatie")
        self.text2.insert(END, "\nGenre: ", 'kopje')
        self.text2.insert(END, self.gescheiden_tekst, 'informatie')
        self.text2.insert(END, "\nSynopsis: ", 'kopje')
        self.text2.insert(END, self.film["synopsis"], 'informatie')
        self.text2.insert(END, "\nDuur: ", 'kopje')
        self.text2.insert(END, self.film["duur"] + " minuten", 'informatie')
        self.text2.insert(END, "\nStarttijd: ", 'kopje')
        self.text2.insert(END, self.tijd + " uur", 'informatie')
        self.text2.insert(END, "\nAanbieder: ", 'kopje')
        self.text2.insert(END, self.film["zender"], 'informatie')
        self.text2.pack()

        #Maakt een knop om de film te reserveren
        self.button1 = Button(self, text="Reserveer deze film", bg="green", fg="white", command=self.verificatie)
        self.button1.pack(side=RIGHT)

        self.pack()
    def verificatie(self):
        """
        Deze functie wordt gebruikt met het knopje "film reserveren". Het vraagt de gebruiker of hij zeker is van zijn invoer. Om vervolgens zijn gegevens in te voeren.
        Als de gebruiker niet zeker is, dan kan hij een andere film reserveren.
        """

        if askyesno("Verify", "Weet je zeker dat je de film wilt reserveren?"):
            if "yes":
                self.informatie_vragen()
        else:
            showinfo("", "U kunt opnieuw kiezen")

    def informatie_vragen(self):
        """
        Deze functie maakt een window waar de gebruiker zijn gegevens in kan voeren. een geeft deze gegevens weer mee
        """
        bezoekers_gegevens.gegevens_vragen(self.film["titel"], self.tijd, self.film["zender"])


    def url_omzetten_naar_jpg(self):
        """
        Deze functie zet een url om naar een jpg bestand. Dit bestand kan vervolgens gebruikt worden in de rest van het bestand
        """
        url = self.film["cover"]
        image_bytes = urlopen(url).read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        pil_image = pil_image.resize((170, 250), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(pil_image)


    def timestamp_omzetten_in_tijd(self):
        """
        Deze functie zorgt ervoor dat de tijdstamp uit de xml omgezet wordt in tijd
        """
        timestamp = self.film["starttijd"]
        self.tijd = datetime.datetime.fromtimestamp(int(timestamp)).strftime("%H:%M")

    def splitten_van_genre(self):
        """
        Deze functie splitst de genre's en plakt ze achter elkaar met ", "
        """
        tekst = self.film["genre"]
        tekst = tekst.split(":")
        self.gescheiden_tekst = ", ".join(tekst)






