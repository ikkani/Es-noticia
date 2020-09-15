from celery	import Celery, task
import tweepy
import api as a
app	=	Celery("tasks",	backend="rpc://",broker="pyamqp://guest@localhost//")

cuantosTuits = 200

@app.task(no_ack = True)
def cargarTuits(choose):
	global cuantosTuits
	if   (choose == 1):
		tuitsElPais 		 =  a.api.user_timeline('elpais_espana',tweet_mode = 'extended', count = cuantosTuits)
		cuantosTuits = 20
		return tuitsElPais
	elif (choose == 2):	
		tuits20m 			 =  a.api.user_timeline('20m',tweet_mode = 'extended', count = cuantosTuits)
		cuantosTuits = 20
		return tuits20m 
	elif (choose == 3):
		tuitsLaVanguardia	 =  a.api.user_timeline('LaVanguardia',tweet_mode = 'extended', count = cuantosTuits)
		return tuitsLaVanguardia
	else:
		tuitsElMundo		 =  a.api.user_timeline('elmundoes',tweet_mode = 'extended', count = cuantosTuits)
		cuantosTuits = 20
		return tuitsElMundo