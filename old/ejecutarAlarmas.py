#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser, json, time

#Se recorren todos los valores de cam_conectadas para indicar si hay alguna desconexión
def camaraDesconectada():
	array_cam = []
	cam_conectadas = configparser.ConfigParser() # abre archivo de configuración
	cam_conectadas.read('/home/xirioxinf/Documentos/descarte_xiriox/csv/cam_conectadas.ini')
	config = configparser.ConfigParser() # abre archivo de configuración
	config.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg')
	cantidad_camaras = config['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema
	try:
		for cam in range(1, int(cantidad_camaras)+1):
			camara_bool = cam_conectadas['CAM']['cam'+str(cam)]
			array_cam.append(camara_bool)
	except Exception as e:
		print(e)
		print('Error cam')
	
	return array_cam

def leerDato(archivoTxt):
	try:
		dato = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/'+archivoTxt+'.txt', 'r')
		datoLeido = dato.read()
		dato.close()
		return datoLeido
	except Exception as e:
		print(e)

def escribirNombreAlarma(alarma, nombre):
	if alarma == 'true':
		arrayAlarmas = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/nombresAlarmas.txt', 'a+')
		arrayAlarmas.write(nombre+'\n')
		arrayAlarmas.close()

while True:
	try:
		camara_alarma = 'false' #Valor que indica si hay alarma o no ['false': no hay alarma, 'true': hay alarma]
		discoFull = 'false'
		sinDiscos = 'false'
		upsFuncionando = 'false'
		apagaManual = 'false'
		apagaUPS = 'false'
		while True:
			arrayAlarmas = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/nombresAlarmas.txt', 'w+')
			arrayAlarmas.write('')
			arrayAlarmas.close()
			array_cameras = camaraDesconectada()
			print(array_cameras)
			if 'false' in array_cameras:
				camara_alarma = 'true'
				AlarmaCamara = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/alarmaCamara.txt', 'w')
				AlarmaCamara.write('true')
				AlarmaCamara.close()
			else:
				if array_cameras != []: # se comprueba que el array no esté vacío
					camara_alarma = 'false'
					AlarmaCamara = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/alarmaCamara.txt', 'w')
					AlarmaCamara.write('false')
					AlarmaCamara.close()
			##############################################
			discoFull = leerDato('discoLleno')
			sinDiscos = leerDato('sinDiscos')
			upsFuncionando = leerDato('upsFuncionando')
			apagaManual = leerDato('apagaManual')
			apagaUPS = leerDato('apagaUPS')

			escribirNombreAlarma(camara_alarma, 'Desconexión Cámara')
			escribirNombreAlarma(discoFull, 'Discos Llenos')
			escribirNombreAlarma(sinDiscos, 'Sin Discos')
			escribirNombreAlarma(upsFuncionando, 'Energía Respaldo Activa')
			escribirNombreAlarma(apagaManual, 'Apagado Manual')
			escribirNombreAlarma(apagaUPS, 'Apagado por UPS')
			print('DISCO: ', discoFull)
			##############################################
			try:
				arrayAlarmas = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/arrayAlarmas.txt', 'w+')
				arrayAlarmas.write((camara_alarma+ ' '+discoFull+ ' '+sinDiscos+ ' '+upsFuncionando+ ' '+ apagaManual+ ' '+ apagaUPS))
				print(camara_alarma, discoFull, sinDiscos, upsFuncionando, apagaManual, apagaUPS)
				arrayAlarmas.close()
			except Exception as e:
				print(e)

			time.sleep(1)

	except Exception as e:
		print("Problema con el servidor")
		print(e)
		#break

	time.sleep(1)
	
