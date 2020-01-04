import cv2
import time
import sys
import threading
import os
import tkinter as tk

img = cv2.imread('/home/xirioxinf/Documentos/descarte_xiriox/gmt_hour/recursos/background.png') # load a dummy image
name = "Config"
global flag_exit
flag_exit = 0

def ventana_actualizando():
	global flag_exit
	while(1):
		cv2.namedWindow(name, cv2.WND_PROP_FULLSCREEN); 
		cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);
		cv2.imshow(name,img)
		
		k = cv2.waitKey(33)
		if k == 225:# si presiona la tecla shif
			#os.system("/home/xirioxinf/Documentos/descarte_xiriox/gmt_hour/cambio_hora")
			#os.system("python3 /home/xirioxinf/Documentos/cambio_hora.py")
			os.system("python3 /home/xirioxinf/Escritorio/encriptar/interfaz_config.py")

		if flag_exit == 1: # si el flag es 1 se cierra
			break
		elif k==-1:  # normally -1 returned,so don't print it
			continue
		else:
			print (k) # else print its value

def actualizando(): # espera por 2 segundos y se cierra
	global flag_exit
	time.sleep(2)
	flag_exit = 1

t = threading.Thread(target=ventana_actualizando, args = ()) # crea el hilo
t2 = threading.Thread(target=actualizando, args = ()) # crea el hilo
t2.setDaemon(False)
t.start() # corre el hilo
t2.start() # corre el hilo