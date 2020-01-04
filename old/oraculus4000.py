import os
import threading
import time
import configparser
import psutil
import hdd_sch
from tkinter import *
import subprocess

#time.sleep(3)
#Proceso de detección de pendrive para actualizar el software
#hddFolder = os.listdir('/media/xirioxinf/')
"""if 'ORAC_UPDATE' in hddFolder:
	os.system('/media/xirioxinf/ORAC_UPDATE/./update')

if 'ORAC_CONFIG' in hddFolder:
	os.system('python3 /media/xirioxinf/ORAC_CONFIG/configuracion.py')"""

os.system("/home/xirioxinf/Documentos/descarte_xiriox/gmt_hour/./tecla") # espera una tecla por 2 seg, sino, sigue normal
#os.system("python3 /home/xirioxinf/Documentos/tecla.py") # espera una tecla por 2 seg, sino, sigue normal
os.system("xtrlock -f")

#time.sleep(4)
#os.system('/home/xirioxinf/Documentos/configuracion/./configuracion')

flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+') #crea el archivo log
flag.write('1')
flag.close()

#time.sleep(7)
#Se montan todas las unidades (discos duros) disponibles en el sistema
unidades = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# intenta montar todas las unidades sda1..sdb2...etc
for x in range(0,len(unidades)):
	os.system('gio mount -d /dev/sd'+unidades[x])
	for z in range(1,5):
		os.system('gio mount -d /dev/sd'+unidades[x]+str(z))

def funcion():
   print ("Excelente")

global ventana # ventana que se muestra mientras carga todo

def loading_window(): # crea la ventana
	global ventana
	# crea y muestra la ventana de carga del software
	ventana = Tk()
	#ventana.after(2000, lambda: ventana.destroy())
	ventana.geometry("400x240")
	imagen = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/loading.png")
	fondo = Label(ventana,image=imagen).place(x=-1,y=-1)
	ventana.wm_attributes('-type', 'splash')
	ventana.mainloop()

#Se selecciona el directorio con todas las unidades montadas
hddFolder = os.listdir('/media/xirioxinf/')
print(hddFolder)

# consulta si hay discos duros montados en el equipo, si está vacio indica que hay un error,
# sino sigue normalmente el sistema
#if hddFolder == []:
if len(hddFolder) <= 3:
	time.sleep(5)
	#proc = subprocess.Popen(['echo xiriox3000 | sudo -S python3 /home/xirioxinf/Documentos/descarte_xiriox/apagar_sin_hdd.py'], shell=True)
	proc = subprocess.Popen(['echo xiriox3000 | sudo -S /home/xirioxinf/Documentos/descarte_xiriox/./apagar_sin_hdd'], shell=True)
	sinDiscos = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
	sinDiscos.write('true')
	sinDiscos.close()
	# crea y muestra la ventana de carga del software
	ventana = Tk()
	#ventana.after(3000, lambda: ventana.destroy())
	ventana.title("Error")
	ventana.geometry("400x240")
	imagen = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/error_discos.png")
	fondo = Label(ventana,image=imagen).place(x=-1,y=-1)
	#boton = Button(ventana, text="Apagar Equipo", command=funcion)
	#boton.place(x = 135, y = 200)
	ventana.wm_attributes('-type', 'splash')
	ventana.mainloop()
else:
	sinDiscos = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
	sinDiscos.write('false')
	sinDiscos.close()

	t = threading.Thread(target=loading_window, args = ()) # crea el hilo
	t.start() # corre el hilo
	
	os.system('/home/xirioxinf/Documentos/descarte_xiriox/./camara_respaldo')
	#os.system('python3 /home/xirioxinf/Documentos/descarte_xiriox/camara_respaldo.py')
	ventana.quit() # después que carga todo cierra la ventana
	
	# comprobar que existan los id del dri y el equipo, sino ejecutar el archivo de configuración antes
	configuracion = configparser.ConfigParser() # abre archivo de configuración
	configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
	if configuracion['ID']['id_dri'] == '' or configuracion['ID']['id_embarcacion'] == '':
		#os.system('python3 /home/xirioxinf/Documentos/configuracion/configuracion.py')
		os.system('/home/xirioxinf/Documentos/configuracion/./configuracion')

	# comprobar que estén todos los discos con sus nombres respectivos
	#lectura_disco = hdd_sch.main()
	hdd_sch.main()
	# ingresar el disco en la configuración (../config/config.cfg)

	#print(lectura_disco)
	#time.sleep(12)

	"""script_array = ['/home/xirioxinf/Documentos/descarte_xiriox/grabar/ejecutar_grabar.py',
					'/home/xirioxinf/Documentos/descarte_xiriox/interfaz/ejecutar_interfaz.py',
					'/home/xirioxinf/Documentos/descarte_xiriox/encriptar/ejecutar_encriptar.py',
					'/home/xirioxinf/Documentos/descarte_xiriox/metadatos/ejecutar_gps.py',
					'/home/xirioxinf/Documentos/descarte_xiriox/arduino/ejecutar_arduino.py',
					'/home/xirioxinf/Documentos/descarte_xiriox/discosInternos.py']"""

	script_array = ['/home/xirioxinf/Documentos/descarte_xiriox/grabar/./ejecutar_grabar',
					#'/home/xirioxinf/Documentos/descarte_xiriox/interfaz/./ejecutar_interfaz',
					'/home/xirioxinf/Documentos/descarte_xiriox/interfaz/./interfaz8',
					'/home/xirioxinf/Documentos/descarte_xiriox/encriptar/./ejecutar_encriptar',
					'/home/xirioxinf/Documentos/descarte_xiriox/metadatos/./ejecutar_gps',
					'/home/xirioxinf/Documentos/descarte_xiriox/arduino/./ejecutar_arduino',
					'/home/xirioxinf/Documentos/descarte_xiriox/./discosInternos',
					'/home/xirioxinf/Documentos/descarte_xiriox/encriptar/./reset_state',
					'/home/xirioxinf/Documentos/descarte_xiriox/./ejecutarAlarmas',
					'/home/xirioxinf/Documentos/descarte_xiriox/./alarmaCamara',
					'/home/xirioxinf/Documentos/descarte_xiriox/./alarmaUPS',
					'/home/xirioxinf/Documentos/descarte_xiriox/./discos_daemon']

	"""script_array = ['/home/xirioxinf/Documentos/descarte_xiriox/interfaz/ejecutar_interfaz.py',
					'/home/xirioxinf/Documentos/descarte_xiriox/arduino/ejecutar_arduino.py']"""

	def script_exe(pos):
		#os.system('python3 '+script_array[pos])
		os.system(script_array[pos])

	for i in range(0,len(script_array)): # ciclo para los hilos
		t = threading.Thread(target=script_exe, args = (i, )) # crea el hilo
		t.start() # corre el hilo
