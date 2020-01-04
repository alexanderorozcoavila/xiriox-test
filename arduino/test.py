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

time.sleep(2)

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
dir_videos = configuracion['Directorios']['dir_videos'] # lee el directorio de videos
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos
id_equipo = configuracion['ID']['id_dri'] # id_equipo

casos_arduino_array = [b'12345\r\n', b'9876\r\n', b'9317\r\n', b'7139\r\n', b'NORMAL\r\n', b'NORMALNORMAL\r\n', b'ALARMA\r\n', b'ALARMAALARMA\r\n']

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
#Lee en el archivo arrayAlarmas.txt si existe alguna alarma en true para indicar al arduino y encender zumbador
flag_silenciar = [False, False, False, False, False, False]

def alarmarSirena(booleano):
	arrayAlarmas = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/arrayAlarmas.txt', 'r+')
	dataa = arrayAlarmas.readline()
	dataa2 = dataa.split(' ')
	#print(dataa2)
	if booleano: # si se presionó el botón silenciar		
		for x in range(0,len(dataa2)):
			if dataa2[x] == 'true':
				flag_silenciar[x] = True
	else: # si no se ha silenciado
		variable_estado = 1
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

# Mantiene esperando por la señal del arduino, desde el botón para detección
# de apagado o si se activa la UPS
a = b'0'
while True:
	try:
		a = arduino.readline() # asgina la lectura de linea del arduino a una variable
		print('-Imprimiendo la línea: ', a)
	except Exception as e:
		print('except')
	
	if a == b'3382\r\n':
		alarmarSirena(True)
	else:
		alarmarSirena(False)
	
	# si detecta el botón (string 12345) se apaga el sistema
	if a == b'12345\r\n':
		print("APAga")
		#apagaSistema()
		break
	# si detecta que se encendió la UPS se detecta el string "9317", espera
	# los 20 min y procese al apagado correcto del equipo.

	# 7139 restablece energía
	if a == b'9317\r\n':
		#alarmarSirena()
		print("UPS EN FUNCIONAMIENTO")
	

		

		count = 0
		# print("Se activó la UPS")
		while True:
			a = arduino.readline() # asgina la lectura de linea del arduino a una variable
			print('Imprimiendo la línea: ', a)
			print('Dentro del while: ', a)
			if a == b'3382\r\n':
				alarmarSirena(True)
			else:
				alarmarSirena(False)
			if a == b'7139\r\n':
				print('Restablece Energía')
				
			if count == 1200: #espera 20min aprox antes de apagarse
				#print("Se apagará el sistema en 20 min")
				print("Se apagó el sistema. UPS")
				break # saca al proceso del ciclo "while"
			else:
				count = count+1

			"""if a == b'3382\r\n':
				print("BOTON")
				alarmarSirena(True)
			else:
				alarmarSirena(False)"""
			if a == b'12345\r\n':
				apagaSistema()
				break
			print(count)

			#time.sleep(1)
# print("Fuera del while")
