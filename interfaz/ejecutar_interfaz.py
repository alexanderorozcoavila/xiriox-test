import os
import configparser

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema

if int(cantidad_camaras) <= 4:
	os.system('/home/xirioxinf/Documentos/descarte_xiriox/interfaz/./interfaz4')
	#os.system('python3 /home/xirioxinf/Documentos/descarte_xiriox/interfaz/interfaz4.py')
else:
	os.system('/home/xirioxinf/Documentos/descarte_xiriox/interfaz/./interfaz8')
	#os.system('python3 /home/xirioxinf/Documentos/descarte_xiriox/interfaz/interfaz8.py')

