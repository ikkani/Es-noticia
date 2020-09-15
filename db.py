import dropbox
import tempfile
import os

dropboxKey = ""

dbx = dropbox.Dropbox(dropboxKey)

def SubirArchivo(archivo,nombreArchivo):
	with open(archivo,'rb') as csvfile:
		dbx.files_upload(csvfile.read(), nombreArchivo, mute=True)

def DescargarArchivo(path):
	dbx.files_download_to_file(os.getcwd()+path, path)

def BorrarArchivo(path):
	dbx.files_delete(path)