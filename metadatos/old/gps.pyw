#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Instalar serial
# pip3 install pyserial
########################################################################
## Se toman los datos del gps y se guardan en un archivo de texto
## dentro de una carpeta temporal ('temp') en el directorio principal usando el protocolo NMEA-0183 el cual entrega los datos de la forma
## $GPRMC,081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E*62 
## Además se genera una archivo que contiene los metadatos que se muestran en el video, éste se
## guarda en el directorio por día
########################################################################
import serial, os, locale, time
import uuid
import configparser
import sys
from serial import Serial
#direc_main = '/home/omvega/Documents/DESCARTE_FINAL_SICAL/descarte_xiriox'
direc_main = '/home/xirioxinf/Documentos/descarte_xiriox'
configuracion = configparser.ConfigParser() # abre archivo de configuración
cam_conectadas = configparser.ConfigParser()
configuracion.read(direc_main+'/config/config.cfg') # lee el archivo de configuración
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos
dir_videos = configuracion['Directorios']['dir_videos'] # lee el directorio de videos
cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema

casos_arduino_array = [b'12345\r\n', b'9876\r\n', b'9317\r\n', b'7139\r\n', b'NORMAL\r\n', b'NORMALNORMAL\r\n', b'ALARMA\r\n', b'ALARMAALARMA\r\n']

if dir_encrypt == '/media/xirioxinf/ERROR':
    sys.exit()

#locale.setlocale(locale.LC_ALL, locale="Spanish")
#locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
##############################################
id_equipo = configuracion['ID']['id_dri'] # obtiene el código único de hardware
##############################################
fecha_dir = time.strftime('%Y-%m-%d') 
path = dir_encrypt+'/'+fecha_dir+'/'
path2 = dir_videos+'/'+fecha_dir+'/'
#os.system('sudo chmod -R 777 /dev') # permisos para linux

def establecerConnect():
    try:
        print('antes MAIN')
        a = serial.Serial("/dev/ttyUSB0", baudrate = 4800)
        print('después MAIN')
        b = a.readline()
        print(b)
        print('antes2 MAIN')
        a.close()
        #if b == b'9876\r\n' or b == b'9317\r\n' or b == b'NORMAL\r\n' or b == b'ALARMA\r\n':
        if b in casos_arduino_array:
            return 'ttyUSB1'
        else:
            return 'ttyUSB0'
    except Exception as e:
        print(e)
        print('antes --')
        a = serial.Serial("/dev/ttyUSB1", baudrate = 4800)
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
print('inicio')
idConnect = establecerConnect()
print('EL RETORNO DE LA FUNCION ES: ', idConnect)
gps = serial.Serial("/dev/"+idConnect, baudrate = 4800) # inicializa el gps dependiendo el puerto COM
#gps = serial.Serial("/dev/ttyUSB1", baudrate = 4800) # inicializa el gps dependiendo el puerto COM

(grados_lat,minutos_lat,segundos_lat) = (0,0,0) 
(grados_lon,minutos_lon,segundos_lon) = (0,0,0)
(rumbo, velocidad) = ('0',0)
lat_sig = "N"
lon_sig = "E"
velocidad = "0.0"

hddFolder = os.listdir('/media/xirioxinf/')
if 'Ext1' in hddFolder or 'Ext2' in hddFolder or 'Ext3' in hddFolder:
	os.makedirs(path+'metadata', exist_ok=True)
	os.makedirs(path2+'metadata', exist_ok=True)

csvfile = open(path+'metadata/METADATA.csv', 'a') # crea un archivo para guardar los metadatos
csvfile.close() # cierra el archivo
csvfile2 = open(path2+'metadata/METADATA.csv', 'a') # crea un archivo para guardar los metadatos
csvfile2.close() # cierra el archivo

if os.stat(path+'metadata/METADATA.csv').st_size == 0:
	csvfile = open(path+'metadata/METADATA.csv', 'a') # crea un archivo para guardar los metadatos
	csvfile.write('Cód. Barco,Fecha,Hora,Latitud,Longitud,Velocidad (nudos),Rumbo (grados),Error (m),CAM 1,CAM 2,CAM 3,CAM 4,CAM 5,CAM 6,CAM 7,CAM 8,CAM 9,CAM 10,CAM 11,CAM 12,CAM 13,CAM 14,CAM 15,CAM 16\n') # primera línea de encabezado de archivo
	csvfile.close() # cierra el archivo 

if os.stat(path2+'metadata/METADATA.csv').st_size == 0:
	csvfile2 = open(path2+'metadata/METADATA.csv', 'a') # crea un archivo para guardar los metadatos
	csvfile2.write('Cód. Barco,Fecha,Hora,Latitud,Longitud,Velocidad (nudos),Rumbo (grados),Error (m),CAM 1,CAM 2,CAM 3,CAM 4,CAM 5,CAM 6,CAM 7,CAM 8,CAM 9,CAM 10,CAM 11,CAM 12,CAM 13,CAM 14,CAM 15,CAM 16\n') # primera línea de encabezado de archivo
	csvfile2.close() # cierra el archivo 
# ciclo que guarda de manera constante cada 1 segundo la información del gps tanto en un archivo gps.txt para la lectura desde las cámaras
# como en el archivo csv para guardar los metadatos
error_gps = 0 #inicialización de error gps

while True:
	time.sleep(1) # tiempo de espera de 1 segundo
	fecha_aux = time.strftime('%Y-%m-%d')
	print(fecha_aux, fecha_dir)
	if fecha_aux != fecha_dir:
		break

	fecha = time.strftime('%d-%m-%Y') 
	hora =  time.strftime('%H:%M:%S') # se obtiene la hora
	line = str(gps.readline())

	#print(line)
	#print(len(line))
	#a = line.split(",") # divide la lectura realizada por comas, dejando los datos separados en un arreglo
	data = line.split(",") # divide la lectura realizada por comas, dejando los datos separados en un arreglo

	if data[0] == "b'$GPGGA":
		print(data)
		try:
			print("El error del gps en metros es: %s" % (data[8]))
			error_gps = float(data[8])
		except Exception as e:
			print(e)
		

	if data[0] == "b'$GPRMC" and len(line) >= 70: # si el 1er
		hora =  time.strftime('%H:%M:%S')
		print(data)
		os.makedirs(path, exist_ok=True) # crea ese nuevo directorio, si existe no pasa nada
		line = str(gps.readline()) # asigna la lectura del gps a "linea" como texto
		#dat dato es de tipo GPRMC toma en cuenta esa lína de datos
		if data[2] == 'A': # 'A' nos indica si el los datos que se toman son válidos
			# Si la latitud es South es negativa, sino la deja positiva
			try:
				#if(data[4] == 'S'):
				grados_lat = int(data[3][0:2])
				if data[4] == "N" or data[4] == "S":
					lat_sig = data[4]
				#else:
					#grados_lat = int(data[3][0:2])
				minutos_lat = int(data[3][2:4])
				segundos_lat = float('0.'+data[3][5:10])*60 # pasa los datos a segundos
				#g_latitud = gdm_to_grados(segundos_lat, minutos_lat, grados_lat)
				# Si la longitud es West es negativa, sino la deja positiva
				"""if(data[6] == 'W'):
					grados_lon = int(data[5][1:3])*-1 # deja la latitud negativa
				else:"""
				grados_lon = int(data[5][1:3])
				if data[6] == "E" or data[6] == "W":
					lon_sig = data[6]
				
				minutos_lon = int(data[5][3:5])
				segundos_lon = float('0.'+data[5][6:11])*60 # pasa los datos a segundos

				try:
					velocidad = float(data[7]) #se asigna la variable velocidad
				except Exception as e:
					print(e)
				
				# si no hay información del rumbo se muestran 2 guiones "--" sino se asigna el rumbo
				if data[8] == '':
					rumbo = '--'
				else:
					rumbo = float(data[8])
			except Exception as e:
				pass			
	else:
		#print("ERROR TOMA DE DATOS")
		pass

	"""fecha2 = time.strftime('%Y-%m-%d')
	path = dir_encrypt+'/'+fecha2+'/'
	os.makedirs(path, exist_ok=True)"""
	#print(path+'metadata/METADATA.csv')
	csvfile = open(path+'metadata/METADATA.csv', 'a') # abre el archivo para guardar los datos
	csvfile2 = open(path2+'metadata/METADATA.csv', 'a') # abre el archivo para guardar los datos
	info_interfaz = open(path+'metadata/metada_temp.csv', 'w') # abre el archivo para guardar los datos
	flag_camaras = ''
	cam_conectadas.read(direc_main+'/csv/cam_conectadas.ini')
	#print(cam_conectadas)
	for i in range(0,int(cantidad_camaras)):
		#flag_camaras.append(cam_conectadas['CAM']['cam'+str(i+1)])
		#print(cam_conectadas['CAM']['cam'+str(i+1)])
		if cam_conectadas['CAM']['cam'+str(i+1)] == 'true':
			try:
				camera = open(direc_main+'/metadatos/info/info_cam'+str(i+1), 'r')
				camera_read = camera.read()
				camera.close()
				flag_camaras = flag_camaras+'%s,     '%camera_read
			except Exception as e:
				flag_camaras = flag_camaras+'--fps - --kbits/s,     '
			
			#print(flag_camaras)
		else:
			flag_camaras = flag_camaras+'--fps - --kbits/s,     '
	#print(flag_camaras)

	# se escriben los datos del gps con el formato para .csv
	csvfile.write(		'%s,     ' % id_equipo+
						'%s,     '%fecha+
						'%s,     '%hora+
						"%d°%d'%.3f" % (grados_lat,minutos_lat,segundos_lat)+'"'+lat_sig+',     '+
						"%d°%d'%.3f" % (grados_lon,minutos_lon,segundos_lon)+'"'+lon_sig+',     '+
						'%s,     '%velocidad+
						'%s°,     '%rumbo+
						'%s,     ' % error_gps+
						flag_camaras+'\n'
				)
	csvfile2.write(		'%s,     ' % id_equipo+
						'%s,     '%fecha+
						'%s,     '%hora+
						"%d°%d'%.3f" % (grados_lat,minutos_lat,segundos_lat)+'"'+lat_sig+',     '+
						"%d°%d'%.3f" % (grados_lon,minutos_lon,segundos_lon)+'"'+lon_sig+',     '+
						'%s,     '%velocidad+
						'%s°,     '%rumbo+
						'%s,     ' % error_gps+
						flag_camaras+'\n'
				)
	info_interfaz.write(		'%s,     ' % id_equipo+
						'%s,     '%fecha+
						'%s,     '%hora+
						"%d°%d'%.3f" % (grados_lat,minutos_lat,segundos_lat)+'"'+lat_sig+',     '+
						"%d°%d'%.3f" % (grados_lon,minutos_lon,segundos_lon)+'"'+lon_sig+',     '+
						'%s,     '%velocidad+
						'%s°,     '%rumbo+'\n'
				)
	csvfile.close() # cierra el archivo
	info_interfaz.close() # cierra el archivo
