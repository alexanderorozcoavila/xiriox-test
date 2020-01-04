import configparser

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('cam_conectadas.ini') # lee el archivo de configuración
while True:
	for i in range(16):
		print(configuracion['CAM']['cam'+str(i+1)]) # lee el directorio de videos