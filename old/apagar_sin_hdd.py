	#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Instalar serial
# pip3 install pyserial

########################################################################
### Se mantiene esperando una respuesta del arduino, cuando
### se presiona el botón de apagado se recibe el string "12345" lo que genera una secuencia de
### pasos para proceder al apagado correcto del equipo. Sí detecta que comienza a funcionar 
### la UPS del sistema se procede a una secuencia de pasos para asegurar un tiempo de 20 minutos
### de grabación sin energía externa, luego se procede con el apagado correcto del equipo manteniendo 
### la integridad de los archivos esperando que finalicen sus tareas antes del apagado.
########################################################################
import serial, os, time
import configparser
from tkinter import *
import threading

time.sleep(2)

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
dir_videos = configuracion['Directorios']['dir_videos'] # lee el directorio de videos
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos
id_equipo = configuracion['ID']['id_dri'] # id_equipo

casos_arduino_array = [b'12345\r\n', b'9876\r\n', b'9317\r\n', b'7139\r\n', b'3382\r\n', b'NORMAL\r\n', b'NORMALNORMAL\r\n', b'ALARMA\r\n', b'ALARMAALARMA\r\n']

def establecerConnect():
    print('antes')
    a = serial.Serial("/dev/ttyUSB0", baudrate = 4800)
    print('después')
    b = a.readline()
    print(b)
    print('antes2')
    a.close()
    #if b == b'9876\r\n' or b == b'9317\r\n' or b == b'NORMAL\r\n' or b == b'ALARMA\r\n':
    if b in casos_arduino_array:
        return 'ttyUSB0'
    else:
        return 'ttyUSB1'

# Establece la conexión con el arduino
print('antes1')
idConnect = establecerConnect()
print('EL RETORNO DE LA FUNCION ES: ', idConnect)
arduino = serial.Serial("/dev/"+idConnect, baudrate = 4800)
#arduino = serial.Serial("/dev/ttyUSB0", baudrate = 9600)
global count
global flag_count
def tiempo_ups(a):
	global count
	global flag_count
	while True:

		time.sleep(1)
		print("EL CONTADOR ES: %s"%count)
		if flag_count == 1: # restablece energía y sale
			break
		if count == 1200: #espera 20min aprox antes de apagarse
			# Se define el tiempo en segundos que se mantiene el sistema funcionando con la UPS
			pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar.txt','r')
			pid_grabar = pid.read()
			pid.close()
			pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar2.txt','r')
			pid_grabar2 = pid.read()
			pid.close()
			print(pid_grabar, pid_grabar2)
			os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar)) # detiene el proceso de grabación
			os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar2)) # detiene el proceso de grabación
			os.system("echo xiriox3000 | sudo -S pkill -f ffmpeg")
			flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+') #crea el archivo log
			flag.write('2')
			flag.close()

			discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/apagaUPS.txt', 'w')
			discoLleno.write('true')
			discoLleno.close()

			ventana = Tk()
			ventana.after(45000, lambda: ventana.destroy())
			ventana.title("Apagando Equipo")
			ventana.geometry("640x400")
			imagen = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/apagando_equipo.png")
			fondo = Label(ventana,image=imagen).place(x=-1,y=-1)
			#boton = Button(ventana, text="Apagar Equipo", command=funcion)
			#boton.place(x = 135, y = 200)
			ventana.wm_attributes('-type', 'splash')
			ventana.mainloop()
			os.system('echo xiriox3000 | sudo -S shutdown -h now')

			print("APAGA SISTEMA POR UPS--")
			# print("Se apagó el sistema.")
			break # saca al proceso del ciclo "while"
		else:
			count = count+1

#Escribe en el archivo correspondiente que no hay alarma
def escribirDato(archivo):
	discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/'+archivo+'.txt', 'w')
	discoLleno.write('false')
	discoLleno.close()
#Lee en el archivo arrayAlarmas.txt si existe alguna alarma en true para indicar al arduino y encender zumbador
flag_silenciar = [False, False, False, False, False, False]

def alarmarSirena(booleano):
	arrayAlarmas = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/arrayAlarmas.txt', 'r+')
	dataa = arrayAlarmas.readline()
	dataa2 = dataa.split(' ')
	#print(flag_silenciar)
	if booleano: # si se presionó el botón silenciar
		# se recorre el array para poner el flag en true(silenciar)		
		for x in range(0,len(dataa2)):
			if dataa2[x] == 'true':
				flag_silenciar[x] = True
	else: # si no se ha silenciado
		variable_estado = 1 # indica si hay alguna alarma activa
		for x in range(0,len(dataa2)):
			if dataa2[x] == 'true':
				variable_estado = 0
			else:
				flag_silenciar[x] = False
		if variable_estado == 0:
			variable_estado_silencio = 1
			for x in range(0,len(dataa2)):
				if dataa2[x] == 'true' and not flag_silenciar[x]:
					variable_estado_silencio = 0
					break

		if variable_estado:
			print("NORMAL")
			arduino.write(b'NORMAL')
		else:
			if variable_estado_silencio:
				print("SILENCIAR")
				arduino.write(b'SILENCIAR')
			else:
				print("ALARMA")
				arduino.write(b'ALARMA')

	arrayAlarmas.close()


	"""if 'true' in dataa:
		arduino.write(b'ALARMA')
	else:
		arduino.write(b'NORMAL')
	print(test)"""
	#arduino.write(b'SILENCIO')

def apagaSistema():
	#alarmarSirena()
	print("APAGA SISTEMA POR BOTÓN")
	discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/apagaManual.txt', 'w')
	discoLleno.write('true')
	discoLleno.close()
	fecha = time.strftime('%Y-%m-%d') # se obtiene la fecha
	hour =  time.strftime('%H:%M:%S') # se obtiene la hora
	### LOG APAGADO POR BOTÓN
	try:
		log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
		log.write(id_equipo+' ['+fecha+' '+hour+']'+" Se apaga el sistema presionando el botón.\n\n")
		log.close()
	except Exception as e:
		pass
	

	pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar.txt','r')
	pid_grabar = pid.read()
	pid.close()												
	pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar2.txt','r')
	pid_grabar2 = pid.read()
	pid.close()
	#print(pid_grabar, pid_encriptar)
	os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar)) # detiene el proceso de grabación
	os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar2)) # detiene el proceso de grabación
	os.system("echo xiriox3000 | sudo -S pkill -f ffmpeg")
	flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+') #crea el archivo log
	flag.write('2')
	flag.close()

	ventana = Tk()
	ventana.after(40000, lambda: ventana.destroy())
	ventana.title("Apagando Equipo")
	ventana.geometry("640x400")
	imagen = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/apagando_equipo.png")
	fondo = Label(ventana,image=imagen).place(x=-1,y=-1)
	#boton = Button(ventana, text="Apagar Equipo", command=funcion)
	#boton.place(x = 135, y = 200)
	ventana.wm_attributes('-type', 'splash')
	ventana.mainloop()

	#time.sleep(15)
	os.system('echo xiriox3000 | sudo -S shutdown -h now')
	print('se apagó---------')

	print("APAGA SISTEMA POR BOTÓN--")
	#break # saca al proceso del ciclo "while"
# Mantiene esperando por la señal del arduino, desde el botón para detección
# de apagado o si se activa la UPS
a = b'0'
while True:
	print("fuera")
	#arduino.close()
	escribirDato('apagaManual')
	escribirDato('upsFuncionando')
	escribirDato('apagaUPS')
	try:
		a = arduino.readline() # asgina la lectura de linea del arduino a una variable
	except Exception as e:
		print('except')
	
	print('Imprimiendo la línea: ', a)
	if a == b'3382\r\n':
		alarmarSirena(True)
	else:
		alarmarSirena(False)
	
	# si detecta el botón (string 12345) se apaga el sistema
	if a == b'12345\r\n':
		apagaSistema()
		break
	# si detecta que se encendió la UPS se detecta el string "9317", espera
	# los 20 min y procese al apagado correcto del equipo.

	# 7139 restablece energía
	if a == b'9317\r\n':
		#alarmarSirena()
		print("UPS EN FUNCIONAMIENTO")
		discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/upsFuncionando.txt', 'w')
		discoLleno.write('true')
		discoLleno.close()
		### LOG UPS
		fecha = time.strftime('%Y-%m-%d') # se obtiene la fecha
		hour =  time.strftime('%H:%M:%S') # se obtiene la hora
		print(hour)
		try:
			log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a+') #crea el archivo log
			log.write(id_equipo+' ['+fecha+' '+hour+']'+" Corte de energía, entra en funcionamiento la UPS.\n\n")
			log.close()
		except Exception as e:
			pass
		
		# print("Se activó la UPS")
		global count
		global flag_count 
		count = 0
		flag_count = 0
		while True:
			a = arduino.readline() # asgina la lectura de linea del arduino a una variable
			print('Imprimiendo la línea: ', a)
			print('Dentro del while: ', a)
			if a == b'3382\r\n':
				alarmarSirena(True)
			else:
				alarmarSirena(False)
			if a == b'7139\r\n':
				flag_count = 1
				print('Restablece Energía')
				
				### LOG UPS
				fecha = time.strftime('%Y-%m-%d') # se obtiene la fecha
				hour =  time.strftime('%H:%M:%S') # se obtiene la hora
				try:
					log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
					log.write(id_equipo+' ['+fecha+' '+hour+']'+" Se reestablece el suministro de energía.\n\n")
					log.close()
				except Exception as e:
					pass
				
				break
			
			if count == 0:
				count = 1
				print("!!!-----------------------------------ENTRA AL HILO!!!-----------------------------------")
				t = threading.Thread(target=tiempo_ups, args = (a, )) # crea el hilo
				t.start() # corre el hilo


			"""if a == b'3382\r\n':
				print("BOTON")
				alarmarSirena(True)
			else:
				alarmarSirena(False)"""
			if a == b'12345\r\n':
				apagaSistema()
				break
			#print(count)

			#time.sleep(1)
# print("Fuera del while")
