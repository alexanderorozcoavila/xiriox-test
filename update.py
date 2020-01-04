import os
from tkinter import *
import threading
import time

global ventana

"""def reiniciando():
	print("222")
	ventana2 = Toplevel()
	#ventana.after(45000, lambda: ventana.destroy())
	ventana2.title("Apagando Equipo")
	ventana2.geometry("640x400")
	imagen2 = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/alarmaUPS.png")
	fondo2 = Label(ventana2,image=imagen2).place(x=-1,y=-1)
	#boton = Button(ventana, text="Apagar Equipo", command=funcion)
	#boton.place(x = 135, y = 200)
	ventana2.wm_attributes('-type', 'splash')
	ventana2.mainloop()"""

def ventana_actualizando():
	global ventana
	#time.sleep(2)
	ventana = Tk()
	#ventana.after(45000, lambda: ventana.destroy())
	ventana.title("Actualizando Equipo")
	ventana.geometry("640x400")
	imagen = PhotoImage(file="/media/xirioxinf/ORAC_UPDATE/recursos/update.png")
	fondo = Label(ventana,image=imagen).place(x=-1,y=-1)
	ventana.wm_attributes('-type', 'splash')
	ventana.wm_attributes("-topmost", True)
	#ventana.wm_attributes("-fullscreen", True)
	ventana.mainloop()
	print("asdasd")
	os.system("python3 /media/xirioxinf/ORAC_UPDATE/update_reiniciando.py")
	#ventana2 = Tk()
	
	

def actualizando():
	global ventana
	print("ELIMINANDO")
	os.system('echo xiriox3000 | sudo -S rm -rf /home/xirioxinf/Descargas/descarte_xiriox') # elimina la carpeta configuración
	os.system('echo xiriox3000 | sudo -S rm -rf /home/xirioxinf/Descargas/configuracion') # elimina la carpeta descarte_xiriox
	print("COPIANDO Y PEGANDO")
	try:
		os.system('cp -r /media/xirioxinf/ORAC_UPDATE/descarte_xiriox /home/xirioxinf/Descargas') # copia la carpeta configuración
		print("car 1 listo")
		os.system('cp -r /media/xirioxinf/ORAC_UPDATE/configuracion /home/xirioxinf/Descargas') # copia la carpeta descarte_xiriox
		print("car 2 listo")
	except Exception as e:
		print(e)
		
	time.sleep(5)
	#reiniciando()
	ventana.destroy()
	print("después quit")

	

"""os.system('echo xiriox3000 | sudo -S rm -rf /home/xirioxinf/Descargas/carpeta1') # elimina la carpeta configuración
os.system('echo xiriox3000 | sudo -S rm -rf /home/xirioxinf/Descargas/carpeta2') # elimina la carpeta descarte_xiriox

os.system('cp -r /media/xirioxinf/ORAC_UPDATE/carpeta1 /home/xirioxinf/Descargas') # copia la carpeta configuración
os.system('cp -r /media/xirioxinf/ORAC_UPDATE/carpeta2 /home/xirioxinf/Descargas') # copia la carpeta descarte_xiriox"""


t = threading.Thread(target=ventana_actualizando, args = ()) # crea el hilo
t2 = threading.Thread(target=actualizando, args = ()) # crea el hilo
t2.setDaemon(False)
t.start() # corre el hilo
t2.start() # corre el hilo


