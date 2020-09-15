import csv
import string
import shutil as sh
import matplotlib.pyplot as plt
import db
from datetime import date 
from datetime import timedelta



ElPais_lista  		= []
XXMin_lista 		= []
ElMundo_lista 		= []
LaVanguardia_lista  = []

cuantosTuits = 200


def copiaDeSeguridad():
	sh.copyfile('ElPais.csv', 'ElPais-copia.csv')
	sh.copyfile('20Min.csv', '20Min-copia.csv')
	sh.copyfile('ElMundo.csv', 'ElMundo-copia.csv')
	sh.copyfile('LaVanguardia.csv', 'LaVanguardia-copia.csv')


def cargarDeCopia():
	sh.copyfile('ElPais-copia.csv', 'ElPais.csv')
	sh.copyfile('20Min-copia.csv', '20Min.csv')
	sh.copyfile('ElMundo-copia.csv', 'ElMundo.csv')
	sh.copyfile('LaVanguardia-copia.csv', 'LaVanguardia.csv')
	cargarListas()


def cargarListas():
	global ElPais_lista
	global XXMin_lista
	global ElMundo_lista
	global LaVanguardia_lista
	db.DescargarArchivo('/ElPais.csv')
	db.DescargarArchivo('/20Min.csv')
	db.DescargarArchivo('/ElMundo.csv')
	db.DescargarArchivo('/LaVanguardia.csv')
	ElPais_lista = csvtolist('ElPais.csv')
	XXMin_lista = csvtolist('20Min.csv')
	ElMundo_lista = csvtolist('ElMundo.csv')
	LaVanguardia_lista = csvtolist('LaVanguardia.csv')


def escritorSeguro(nombrefichero, tuit):
	with open(nombrefichero,'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([tuit[0], tuit[1], tuit[2], tuit[3] ])
	db.BorrarArchivo('/'+nombrefichero)
	db.SubirArchivo(nombrefichero,'/'+nombrefichero)
	
		
def formatearCadena(cadena):
	cadena = cadena.replace('.',' ')
	cadena = cadena.replace(',',' ')
	cadena = cadena.replace('(',' ')
	cadena = cadena.replace(')',' ')
	cadena = cadena.replace('\'',' ')
	cadena = cadena.replace(':',' ')
	cadena = cadena.replace('’',' ')
	cadena = cadena.replace('‘',' ')
	return cadena

#Recibe 'nombre.csv'
#Devuelve una lista con el contenido de cada fila

def csvtolist(nombrefichero):
	with open(nombrefichero, 'r') as csvfile:	
		lista = []
		reader = csv.reader(csvfile)
		for elemento in reader:
			lista_aux =[]
			cadena   = elemento[0]
			cadena   = formatearCadena(cadena)
			lista_aux.append(cadena)
			lista_aux.append(elemento[1])
			lista_aux.append(elemento[2])
			lista_aux.append(elemento[3])
			lista.append(lista_aux)
		return lista


def buscarPalabra(PalabraBuscada, dias):
	nElPais		  = 0
	nXXmin   	  = 0
	nElMundo 	  = 0
	nLaVanguardia = 0

	FechaUmbral = date.today() - timedelta(days=dias)

	for noticia in ElPais_lista:
		spliteado = noticia[0].split()
		for palabra in spliteado:
			if palabra.lower() == PalabraBuscada.lower():
				FechaNoticia = date(int(noticia[3]), int(noticia[2]), int(noticia[1]))
				if (FechaNoticia >= FechaUmbral):
					nElPais += 1

	for noticia in XXMin_lista:
		spliteado = noticia[0].split()
		for palabra in spliteado:
			if palabra.lower() == PalabraBuscada.lower():
				FechaNoticia = date(int(noticia[3]), int(noticia[2]), int(noticia[1]))
				if (FechaNoticia >= FechaUmbral):
					print (noticia[0])
					nXXmin += 1

	for noticia in ElMundo_lista:
		spliteado = noticia[0].split()
		for palabra in spliteado:
			if palabra.lower() == PalabraBuscada.lower():
				FechaNoticia = date(int(noticia[3]), int(noticia[2]), int(noticia[1]))
				if (FechaNoticia >= FechaUmbral):
					nElMundo += 1

	for noticia in LaVanguardia_lista:
		spliteado = noticia[0].split()
		for palabra in spliteado:
			if palabra.lower() == PalabraBuscada.lower():
				FechaNoticia = date(int(noticia[3]), int(noticia[2]), int(noticia[1]))
				if (FechaNoticia >= FechaUmbral):
					nLaVanguardia += 1


	lista = [['El pais', nElPais],['20 min', nXXmin], ['El Mundo', nElMundo], ['La vanguardia', nLaVanguardia]]

	return lista


def plotPalabra(palabra, dias = 1):
	lista = buscarPalabra(palabra, dias)
	nElPais 	  = lista[0][1]
	nXXmin   	  = lista[1][1]
	nElMundo 	  = lista[2][1]
	nLaVanguardia = lista[3][1]

	vRep = [nElPais, nXXmin, nElMundo, nLaVanguardia]

	p1, p2, p3, p4 = plt.bar([lista[0][0], lista[1][0], lista[2][0], lista[3][0]] , vRep )
	p1.set_facecolor('goldenrod')
	p2.set_facecolor('gold')
	p3.set_facecolor('orange')
	p4.set_facecolor('orangered')
	plt.ylim(0, max(vRep)+3)
	plt.title('Repeticiones de la palabra: '+ palabra + ' , en los últimos ' + str(dias) + ' días.')
	plt.savefig('grafica.png', bbox_inches='tight')
	plt.clf()


def rellenarCSV(nombreFichero, tuits):
	for tuit in tuits:
		a = buscarTuit(nombreFichero, tuit.full_text)
		if (a == -1):
			lista = []
			texto = (tuit.full_text)
			date  = tuit.created_at
			lista = [texto, date.day, date.month, date.year] 
			escritorSeguro(nombreFichero,lista)


def buscarTuit(nombre, tuit):
	tuit = formatearCadena(tuit)
	if (nombre == 'ElPais.csv'):
		for elemento in ElPais_lista:
			if (elemento[0] == tuit):
				return ElPais_lista.index(elemento)
		return -1
	elif (nombre == '20Min.csv'):
		for elemento in XXMin_lista:
			if (elemento[0] == tuit):
				return XXMin_lista.index(elemento)
		return -1

	elif (nombre == 'ElMundo.csv'):
		for elemento in ElMundo_lista:
			if (elemento[0] == tuit):
				return ElMundo_lista.index(elemento)
		return -1

	elif (nombre == 'LaVanguardia.csv'):
		for elemento in LaVanguardia_lista:
			if (elemento[0] == tuit):
				return LaVanguardia_lista.index(elemento)
		return -1

	else: print ("Nombre de fichero incorrecto en la funcion\"buscarTuit(nombre, tuit)\"")


def csvmencionestolist():
	db.DescargarArchivo('/Menciones.csv')
	with open('Menciones.csv', 'r') as csvfile:	
		lista = []
		reader = csv.reader(csvfile)
		for elemento in reader:
			cadena   = elemento[0]
			lista.append(cadena)
		return lista


def comprobarFormatoMenciones(lista_menciones):
	lista_buenas_menciones = []
	for mencion in lista_menciones:
		spliteado = mencion.text.split()
		if(len(spliteado) < 2):
			pass
		elif(len(spliteado) > 3):
			pass
		else:
			lista_buenas_menciones.append(mencion)

	return lista_buenas_menciones


def contestarTuits(lista_menciones,api):
	lista_menciones = comprobarFormatoMenciones(lista_menciones)
	dias = 1
	for mencion in lista_menciones:
		spliteado = mencion.text.split()
		if(len(spliteado) > 2):
			if (str(spliteado[2]).isnumeric()):
				dias = int(spliteado[2])

		plotPalabra(spliteado[1], dias)
		api.update_with_media(status = ('@'+mencion.user.screen_name), filename = 'grafica.png', in_reply_to_status_id = mencion.id)


def nuevasMenciones(api):
	lista_nuevasMenciones = []
	
	menciones = api.mentions_timeline()
	lista_menciones = csvmencionestolist()
	
	for mencion in menciones:
		esta = lista_menciones.count(mencion.id_str)
		if (esta < 1):
			lista_nuevasMenciones.append(mencion)
	nuevasMencionesAFichero(menciones)

	return lista_nuevasMenciones


def nuevasMencionesAFichero(lista_menciones):
	with open('Menciones.csv','a') as csvfile:
		writer = csv.writer(csvfile)
		for elemento in lista_menciones:
			writer.writerow([elemento.id_str])
	db.BorrarArchivo('/Menciones.csv')
	db.SubirArchivo('Menciones.csv','/Menciones.csv')



cargarListas()