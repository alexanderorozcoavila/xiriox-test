import os
import psutil
import time
import configparser

direcFolder = '/home/xirioxinf/'

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
cant_discos = configuracion['Externos']['cant_discos']

def formatHdd(hddFolder, ext):
	dps = psutil.disk_partitions()
	for i in dps:
		#print(i)
		if i[1] == hddFolder:
			os.system('echo xiriox3000 | sudo -S umount '+i[0])
			time.sleep(0.5)
			os.system('echo xiriox3000 | sudo -S umount '+i[0])
			time.sleep(0.5)
			os.system('echo xiriox3000 | sudo -S mkfs.exfat -n "'+ext+'" '+i[0])
			time.sleep(0.5)
			os.system('gio mount -d '+i[0])
			#os.system('gio mount -d '+i[0])
			#return i[0]

def sortSecond(val): 
    return val[1]  

def porcentajes(externalHdd):
	# comparar el % de disco ocupado

	hddFolder = os.listdir(direcFolder)
	print("hddFolder ", hddFolder)
	porcentajes = []
	for porc in hddFolder:
		if porc in externalHdd:
			porcentajes.append([psutil.disk_usage(direcFolder+porc)[3], porc])

	porcentajes.sort(key = sortSecond)
	#porcentajes[0][0] = 95.1
	print('Porcentajes: ', porcentajes)

	discoActual = 'ERROR'
	for indice in range(0, int(cant_discos)):
		if float(porcentajes[indice][0]) < 95 and porcentajes[indice][1] in externalHdd:
			discoActual = porcentajes[indice][1]
			break
	"""for indice in porcentajes:
		if float(indice[0]) < 95 and indice[1] in externalHdd:
			discoActual = indice[1]
			break"""

	# acá se cambia el disco duro de encriptación en la configuración
	print("El disco duro a usar es: '%s'" % discoActual)

	return(discoActual)


def main():
	#Nombres discos externos e internos
	externalHdd = ['Ext1', 'Ext2', 'Ext3']
	internalHdd = ['Int1', 'Int2', 'Int3']

	# obtiene los nombres de los discos montados en el directorio
	hddFolder = os.listdir(direcFolder)
	print(hddFolder)
	print('\n')

	# comprobar la existencia de las unidades y el formateo para definir el nombre
	for i in range(0, len(hddFolder)):
		print('hddFolder: ',hddFolder)
		if hddFolder[i] in externalHdd or hddFolder[i] in internalHdd:
			# se puede negar el in anterior y saltar el "else"
			print('Existe la unidad: %s' % hddFolder[i])
		else:
			for ext in externalHdd:
				if ext in hddFolder:
					# se puede negar el in anterior y saltar el "else"
					print('Ya existe ', ext)
				else:
					print("Se formatea la unidad: [%s] como %s" % (hddFolder[i],ext))
					print(direcFolder+hddFolder[i])
					#os.system('sudo mv -v '+direcFolder+hddFolder[i]+' '+direcFolder+ext) # se debe formatear
					formatHdd(direcFolder+hddFolder[i], ext)
					#os.system('gio mount -d '+disco_stu)
					hddFolder = os.listdir(direcFolder)
					break

	porcen = porcentajes(internalHdd)
	#print(porcen)
	

	configuracion['Directorios']['dir_videos'] = direcFolder+porcen
	with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
		configuracion.write(configfile)
	
	porcen = porcentajes(externalHdd)
	#print(porcen)
	configuracion = configparser.ConfigParser() # abre archivo de configuración
	configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración

	configuracion['Directorios']['dir_encrypt'] = direcFolder+porcen
	with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
		configuracion.write(configfile)

if __name__ == '__main__':
	main()
