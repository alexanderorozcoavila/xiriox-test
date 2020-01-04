import configparser
import os

valor_sin_camara = "55" # def el valor si no hay una cámara conectada en esa posición

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
cant_camaras = int(configuracion['Videos']['cantidad_camaras']) # lee la cantidad de cámaras 

camaras_fijas = ["71","72","73","74","75","76"] # ip de las cámaras que son fijas del sistema
camaras_repuesto = ["91","92","93","94","95","96"] # ip de las cámaras de repuesto

flag_camaras = [] #contiene la ip de las cámaras para mostrar
flag_camaras_rep = []#contiene la ip de las cámaras de respuesto disponibles

#agrega las camaras de repuesto que están conectadas
for i in range(0, cant_camaras):
	respuesta = os.system("ping -c 1 10.1.1."+str(camaras_repuesto[i]))
	if respuesta == 0:
		flag_camaras_rep.append(camaras_repuesto[i])
	else:
		respuesta = os.system("ping -c 1 10.1.1."+str(camaras_repuesto[i]))
		if respuesta == 0:
			flag_camaras_rep.append(camaras_repuesto[i])

if len(flag_camaras_rep) == 0:
	camaras_fijas = ["71","72","73","74","75","76"] # ip de las cámaras que son fijas del sistema
else:
	flag_camaras_rep = []#contiene la ip de las cámaras de respuesto disponibles
	############################################################################
	#agrega las camaras fijas que están conectadas
	for i in range(0, cant_camaras):
		respuesta = os.system("ping -c 1 10.1.1."+str(camaras_fijas[i]))
		if respuesta == 0:
			flag_camaras.append(camaras_fijas[i])
		else:
			respuesta = os.system("ping -c 1 10.1.1."+str(camaras_fijas[i]))
			if respuesta == 0:
				flag_camaras.append(camaras_fijas[i])
			else:
				flag_camaras.append(valor_sin_camara)
	##########################################################################
	#agrega las camaras de repuesto que están conectadas
	for i in range(0, cant_camaras):
		respuesta = os.system("ping -c 1 10.1.1."+str(camaras_repuesto[i]))
		if respuesta == 0:
			flag_camaras_rep.append(camaras_repuesto[i])
		else:
			respuesta = os.system("ping -c 1 10.1.1."+str(camaras_repuesto[i]))
			if respuesta == 0:
				flag_camaras_rep.append(camaras_repuesto[i])
	##########################################################################
	#si hay camaras fijas desconectadas, las reemplaza por las de repuesto
	for i in range(0, flag_camaras.count("55")):
		try:
			flag_camaras[flag_camaras.index('55')] = flag_camaras_rep[i]
		except Exception as e:
			print(e)
	##########################################################################
print(flag_camaras)
print(flag_camaras_rep)
#guarda los valores de las camaras en el archivo de configuración
for i in range(0, cant_camaras):
		configuracion['IP']['cam'+str(i+1)] = flag_camaras[i]
with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
	configuracion.write(configfile)

	