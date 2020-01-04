import cron
import time
import configparser
import threading
import json
import requests
import os
import sys
import recopDatos

time.sleep(5)
configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
#dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos
dir_videos = configuracion['Directorios']['dir_videos'] # lee el directorio de videos
cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema

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

num_cam = sys.argv[1]
contador_sub = 1
cambio_segundo = time.strftime('%S')
minu = 0
seg = 0
minu2 = 0
seg2 = 1
fecha = time.strftime('%Y-%m-%d') # se obtiene la fecha
path = dir_videos+'/'+fecha+'/CAM'+num_cam+'/' # directorio de la cámara
#path_encrypt = dir_encrypt+'/'+fecha+'/CAM'+num_cam+'/'
ult_video = ultimo_video(num_cam, fecha) # obtiene el último archivo que se está grabado (el actual)
nombre_ult_video = ult_video.split(".")[0] # guarda el nombre del último video sin la extensión ".mp4"
while True:
    request = recopDatos.index()
    request = json.loads(request)

    cambio_segundo_aux = cambio_segundo
    cambio_segundo = time.strftime('%S')
    if cambio_segundo != cambio_segundo_aux:
        sub = open(path+nombre_ult_video+".srt", "a")
        minu, seg, seg_str, min_str, minu2, seg2, min_str2, seg_str2 = cron.min_seg(minu, seg, minu2, seg2)
        sub.write(
            str(contador_sub)+'\n'+
            '00:'+min_str+seg_str+' --> '+ '00:'+min_str2+seg_str2+'\n'+
            request['id']['id_dri']+'\n'+
            request['id']['id_embarcacion']+'\n'+
            request['gps']['fecha']+'\n'+
            request['gps']['hora']+'\n'+
            request['gps']['latitud']+'\n'+
            request['gps']['longitud']+'\n'+
            request['gps']['rumbo']+'°\n'+
            request['gps']['velocidad']+'\n\n'
            )
        contador_sub = contador_sub+1
    #os.system('cp '+path+nombre_ult_video+".srt "+path_encrypt+nombre_ult_video+".srt")
    print(str(minu2)+':'+str(seg2))
    if str(minu2) == '59' and str(seg2) == '59':
        break
    time.sleep(0.5)
print("SALE: ", str(num_cam))
