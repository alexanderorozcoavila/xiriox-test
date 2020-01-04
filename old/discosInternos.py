import os, psutil, configparser, time
import sys
sys.path.insert(0, '/home/xirioxinf/Documentos/descarte_xiriox')
import hdd_sch

internalHdd = ['Int1', 'Int2', 'Int3']

#Elimina el primer elemento de la lista en el txt
def eliminarPrimero():
	listaCarpetas = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/listaCarpetas.txt','r+')
	primeraCarpeta = listaCarpetas.readlines()
	print('primeraCarpeta: ')
	print(primeraCarpeta)
	del primeraCarpeta[0]
	print('primeraCarpeta: ')
	print(primeraCarpeta)
	listaCarpetas.close()
	################################
	listaCarpetas = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/listaCarpetas.txt','w')
	listaCarpetas.writelines(primeraCarpeta)
	listaCarpetas.close()

#Elimina la carpeta más antigua en la lista
def eliminarCarpeta():
	listaCarpetas = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/listaCarpetas.txt','r+')
	primeraCarpeta = listaCarpetas.readline()
	print('primeraCarpeta: ')
	print(primeraCarpeta)
	os.system('echo xiriox3000 | sudo -S rm -rf '+primeraCarpeta)
	listaCarpetas.close()
	print('Se elimina la carpeta')
	primeraCarpetaAux = primeraCarpeta
	eliminarPrimero()
	while primeraCarpeta == primeraCarpetaAux:
		listaCarpetas = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/listaCarpetas.txt','r+')
		primeraCarpetaAux = listaCarpetas.readline()
		print('primeraCarpetaAux: ')
		print(primeraCarpetaAux)
		listaCarpetas.close()


while True:
	porcen = hdd_sch.porcentajes(internalHdd)
	print('porcen: ', porcen)
	time.sleep(1)
	"""configuracion = configparser.ConfigParser() # abre archivo de configuración
	configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
	dir_encrypt = configuracion['Directorios']['dir_videos'] # lee el directorio de videos

	disco_duro = psutil.disk_usage(dir_encrypt)#cambiar directorio para detección de disco 
	espacioDisponible = str(disco_duro[3])+'% HDD Ocupado' #Mostrar espacio libre en GB"""

	if porcen == 'ERROR':
		eliminarCarpeta()
		
	#print(espacioDisponible)