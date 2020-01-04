#!/usr/bin/env python
# éste script se ejecuta con ejecutar_grabar.py
import os
import time
import threading
import configparser
import psutil
import hdd_sch
import hashlib
import sys
import subprocess

externalHdd = ['Ext1', 'Ext2', 'Ext3']
porcenExt = hdd_sch.porcentajes(externalHdd)
print(porcenExt)
if porcenExt == 'ERROR':
    discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
    discoLleno.write('true')
    discoLleno.close()
else:
    discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
    discoLleno.write('false')
    discoLleno.close()
configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración

"""internalHdd = ['Int1', 'Int2', 'Int3']
porcenInt = hdd_sch.porcentajes(internalHdd)
print('GRABAR + '+porcenInt)
configuracion['Directorios']['dir_videos'] = '/media/xirioxinf/'+porcenInt"""
configuracion['Directorios']['dir_encrypt'] = '/home/xirioxinf/'+porcenExt
with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
    configuracion.write(configfile)

dir_videos = configuracion['Directorios']['dir_videos'] # lee el directorio de videos
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos

if dir_encrypt == '/media/xirioxinf/ERROR':
    sys.exit()

tiempo_minimo_error = int(configuracion['Videos']['tiempo_minimo_error']) # tiempo en segundos que demora para que indique que hay un error con la cámara
tiempo_grabacion_videos = configuracion['Videos']['tiempo_grabacion_videos'] # hh:mm:ss
cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema
id_equipo = configuracion['ID']['id_dri'] # id_equipo
id_embarcacion = configuracion['ID']['id_embarcacion'] # id_equipo

pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar2.txt','w+')
pid.write(str(os.getpid()))
pid.close()

fecha = time.strftime('%Y-%m-%d') # se obtiene la fecha
listaCarpetas = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/listaCarpetas.txt','r+')
try:
    ultimaCarpeta = listaCarpetas.readlines()[-1]
except Exception as e:
    ultimaCarpeta = ''
print('ultimaCarpeta: ')
print(ultimaCarpeta)
print(dir_videos+'/'+fecha)

if ultimaCarpeta != dir_videos+'/'+fecha and dir_videos != '/home/xirioxinf/ERROR':
    print('Distintos')    
    listaCarpetas.write('\n'+dir_videos+'/'+fecha)
else:
    print('Ya está la fecha')
listaCarpetas.close()

# Genera un archivo MD5 de cada archivo grabado para verficar 
# la integridad de los datos posteriormente
def hasher_md5(archivo_hash, archivo_md5):
    BLOCKSIZE = 65536 # Se define el tamaño de un bloque para lectura
    hasher = hashlib.md5() # Define "hasher" como datos md5
    with open(archivo_hash, 'rb') as afile: # abre el archivo para analizar como lectura (se renombra como "afile")
        buf = afile.read(BLOCKSIZE) # Obtiene un bloque de datos y lo almacena en un buffer
        # (ciclo while de abajo)Si la longitud del buffer es mayor a cero sigue analizando, si no es mayor a cero
        # quiere decir que no hay más datos en archivo (se llegó al final)
        while len(buf) > 0: 
            hasher.update(buf) # guarda el cálculo realizado del buffer en "hasher"
            buf = afile.read(BLOCKSIZE) # Vuelve a obtener otro bloque de datos para seguir almacenando los datos dentro del "while"
    f = open(archivo_md5, "w") # abre el archivo (es un txt pasado por parámetro) como escritura
    # se escribe el cálculo del md5 realizado en el archivo y directorio
    # donde se deja el archivo encriptado
    f.write(str(hasher.hexdigest()).upper()) 
    f.close() # Se cierra el archivo para un correcto guardado de éste
    #print(hasher.hexdigest())

# Detecta el último video que se está grabando dentro de la carpeta de la cámara
def ultimo_video(num, fecha):
    lista = [] # Lista vacia para agregar elementos
    files = os.listdir(dir_videos+'/'+fecha+'/CAM'+num+'/') # Obtiene todos los archivos del directorio de la cámara
    #Recorrer los archivos del directorio obtenido 
    for fichero in files:
        # Comprueba que sea distinto a las carpetas del directorio
        # ya que no tienen extensión por lo tanto no se puede hacer un split 
        # y eso genera error en la linea siguiente de código
        if fichero != "thumbs" and fichero != "grabs" and fichero != "md5":  
            split = fichero.split(".") # Dividir extensión y nombre de archivo
            #print(split)
            if split[1] == "mp4": # Si la extensión es "mp4" ingresa el archivo a la lista
                lista.append(fichero) # Agrega elemento a la lista
    lista.sort(reverse=True) # Ordena la lista de mayor a menor obteniendo el último archivo al principio de la lista
    return lista[0] # Retorna el primer elemento de la lista ordenada, el cual sería el último archivo grabado

# método que graba la cámara directactamente
def grabando(num_ip, num_cam):
    fecha = time.strftime('%Y-%m-%d') # se obtiene la fecha
    hora =  time.strftime('%H-%M-%S') # se obtiene la hora
    hour =  time.strftime('%H:%M:%S') # se obtiene la hora
    path = dir_videos+'/'+fecha+'/CAM'+num_cam+'/' # directorio de la cámara
    path_encrypt = dir_encrypt+'/'+fecha+'/CAM'+num_cam+'/'
    os.makedirs(path, exist_ok=True) # crea el directorio, si ya existe no hace nada
    os.makedirs(path_encrypt, exist_ok=True) # crea el directorio, si ya existe no hace nada
    #FILE_OUTPUT = path+'/CAM'+num_cam+'_'+fecha+'_'+hora+'.mp4' # directorio y nombre del archivo de salida
    FILE_OUTPUT = path+'/'+'CAM'+num_cam+'_'+id_embarcacion+'_'+id_equipo+'_'+fecha+'_'+hora+'.mp4'
    ###################################################################################
    ### LOG INICIA GRABACIÓN
    # log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    # log.write(id_equipo+' ['+fecha+' '+hour+']'+" Inicia Grabación CAM"+num_cam+'   IP: 10.1.1.'+num_ip+'\n\n') 
    # log.close()
    ### LOG INICIA GRABACIÓN
    log2 = open (dir_videos+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    log2.write(id_equipo+' ['+fecha+' '+hour+']'+" Inicia Grabación CAM"+num_cam+'   IP: 10.1.1.'+num_ip+'\n\n') 
    log2.close()
    ###################################################################################
    tiempo_inicial = time.time() # guarda el tiempo de inicio
    # ejecuta la consola con el comando ffmpeg
    proc = subprocess.Popen(['python3 /home/xirioxinf/Documentos/descarte_xiriox/scripts/srtVideos.py '+str(num_cam)], shell=True)
    os.system('ffmpeg -t '+tiempo_grabacion_videos+' -rtsp_transport tcp -i rtsp://admin:xiriox3000@10.1.1.'+num_ip+':554 -acodec copy -vcodec copy '+FILE_OUTPUT)
    
    tiempo_final = time.time() # guerda el tiempo final
    tiempo_ejecucion = tiempo_final - tiempo_inicial # guerda el tiempo total de ejecución
    time.sleep(1)
    ###################################################################################
    ### LOG MÓDULO PARA ERROR
    # if (tiempo_ejecucion) < tiempo_minimo_error:
    #     # log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    #     # log.write(id_equipo+' ['+fecha+' '+time.strftime('%H:%M:%S')+']'+" Error CAM"+num_cam+'   IP: 10.1.1.'+num_ip+" - No logra comunicar con la cámara"+'\n\n') 
    #     # log.close()
    #     log2 = open (dir_videos+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    #     log2.write(id_equipo+' ['+fecha+' '+time.strftime('%H:%M:%S')+']'+" Error CAM"+num_cam+'   IP: 10.1.1.'+num_ip+" - No logra comunicar con la cámara"+'\n\n') 
    #     log2.close()
    ###################################################################################
    ### LOG FINALIZA GRABACIÓN
    # log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    # log.write(id_equipo+' ['+fecha+' '+time.strftime('%H:%M:%S')+']'+" Finaliza Grabación CAM"+num_cam+'   IP: 10.1.1.'+num_ip+'\n\n') 
    # log.close()
    ### LOG FINALIZA GRABACIÓN
    log2 = open (dir_videos+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    log2.write(id_equipo+' ['+fecha+' '+time.strftime('%H:%M:%S')+']'+" Finaliza Grabación CAM"+num_cam+'   IP: 10.1.1.'+num_ip+'\n\n') 
    log2.close()
    # genera un archivo md5 del archivo y directorio pasados por parámetro (descomentar la línea de abajo)
    ult_video = ultimo_video(num_cam, fecha) # obtiene el último archivo que se está grabado (el actual)
    nombre_ult_video = ult_video.split(".")[0] # guarda el nombre del último video sin la extensión ".mp4"
    hasher_md5(dir_videos+'/'+fecha+'/CAM'+num_cam+'/'+ult_video, dir_videos+'/'+fecha+'/CAM'+num_cam+'/'+nombre_ult_video+".md5")
    ###################################################################################

#urls = [71,72,73,74] # número para cada cámara en la conexión RTSP
urls = [] # número para cada cámara en la conexión RTSP
for i in range(0,int(cantidad_camaras)):
    urls.append(configuracion['IP']['cam'+str(i+1)])

print(urls)

def main():
    flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+') #crea el archivo log
    flag.write('1')
    flag.close()
    for i in range(0,int(cantidad_camaras)): # ciclo para los hilos
        t = threading.Thread(target=grabando, args = (str(urls[i]), str(i+1))) # crea el hilo
        t.start() # corre el hilo

if __name__ == '__main__':
	main()


