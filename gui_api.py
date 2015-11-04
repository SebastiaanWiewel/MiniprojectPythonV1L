import requests
import xmltodict
from gui_layout import *
import datetime

informatie_dag = datetime.datetime.now()
response = requests.get('http://www.filmtotaal.nl/api/filmsoptv.xml?apikey=smuj9eu02ftqsj9cmh28fmea3hhg0agt&dag=%s-%s-%s&sorteer=0' % (informatie_dag.day, informatie_dag.month, informatie_dag.year))
xml = xmltodict.parse(response.content)
filmsdict = (xml["filmsoptv"]["film"])


root = Tk()
filmlijst = LijstFrame(root, filmsdict)

root.mainloop()
