import configparser

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema

for x in range(0,int(cantidad_camaras)):
	flag = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptarCAM'+str(x+1),'w+') #crea el archivo log
	flag.write('false')
	flag.close()

"""flag = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptarCAM1','w+') #crea el archivo log
flag.write('false')
flag.close()

flag = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptarCAM2','w+') #crea el archivo log
flag.write('false')
flag.close()

flag = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptarCAM3','w+') #crea el archivo log
flag.write('false')
flag.close()"""