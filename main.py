import csv
import string
import shutil as sh
import matplotlib.pyplot as plt
import tweepy
import biblioteca as bt
import os
import time
from celery import group
import bibliotecaCelery as btC
import api as a
bt.copiaDeSeguridad()



peticionesTuit = 10

while True:

	if (peticionesTuit == 10):
		try:
			job1 = btC.cargarTuits.delay(1)
			job2 = btC.cargarTuits.delay(2)
			job3 = btC.cargarTuits.delay(3)
			job4 = btC.cargarTuits.delay(4)
		except:
			time.sleep(60*15)

		
		result1 = job1.get()
		result2 = job2.get()
		result3 = job3.get()
		result4 = job4.get()

		cuantosTuits = 20
		peticionesTuit = -1


		bt.rellenarCSV('ElPais.csv',tuitsElPais)
		bt.rellenarCSV('20Min.csv',tuits20m)
		bt.rellenarCSV('LaVanguardia.csv',tuitsLaVanguardia)
		bt.rellenarCSV('ElMundo.csv',tuitsElMundo)



	peticionesTuit += peticionesTuit 
	menciones = bt.nuevasMenciones(api)
	if (len(menciones) > 0):
		bt.contestarTuits(menciones,api)

	time.sleep(60)

