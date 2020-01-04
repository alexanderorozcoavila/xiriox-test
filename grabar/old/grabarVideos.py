#!/usr/bin/env python
# éste script se ejecuta con ejecutar_grabar.py
import os
import time
import threading
import configparser
import psutil
import hdd_sch

externalHdd = ['Ext1', 'Ext2', 'Ext3']
porcen = hdd_sch.porcentajes(externalHdd)
print(porcen)
if porcen == 'ERROR':
    discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
    discoLleno.write('true')
    discoLleno.close()
else:
    discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
    discoLleno.write('false')
    discoLleno.close()
configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración

internalHdd = ['Int1', 'Int2', 'Int3']
porcenInt = hdd_sch.porcentajes(internalHdd)
print('GRABAR + '+porcenInt)
configuracion['Directorios']['dir_videos'] = '/media/xirioxinf/'+porcenInt
#configuracion['Directorios']['dir_encrypt'] = '/media/xirioxinf/'+porcen
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
if ultimaCarpeta != dir_videos+'/'+fecha and dir_videos != '/media/xirioxinf/ERROR':
    print('Distintos')    
    listaCarpetas.write('\n'+dir_videos+'/'+fecha)
else:
    print('Ya está la fecha')
listaCarpetas.close()
# método que graba la cámara directactamente
def grabando(num_ip, num_cam):
    #while True:
    fecha = time.strftime('%Y-%m-%d') # se obtiene la fecha
    hora =  time.strftime('%H-%M-%S') # se obtiene la hora
    hour =  time.strftime('%H:%M:%S') # se obtiene la hora
    path = dir_videos+'/'+fecha+'/CAM'+num_cam+'/' # directorio de la cámara
    path_encrypt = dir_encrypt+'/'+fecha+'/CAM'+num_cam+'/'
    os.makedirs(path, exist_ok=True) # crea el directorio, si ya existe no hace nada
    os.makedirs(path_encrypt, exist_ok=True) # crea el directorio, si ya existe no hace nada
    #FILE_OUTPUT = path+'/CAM'+num_cam+'_'+fecha+'_'+hora+'.mp4' # directorio y nombre del archivo de salida
    FILE_OUTPUT = path+'/'+id_embarcacion+'_'+id_equipo+'_'+fecha+'_'+hora+'.mp4'
    ###################################################################################
    ### LOG INICIA GRABACIÓN
    log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    log.write(id_equipo+' ['+fecha+' '+hour+']'+" Inicia Grabación CAM"+num_cam+'   IP: 10.1.1.'+num_ip+'\n\n') 
    log.close()
    ### LOG INICIA GRABACIÓN
    log2 = open (dir_videos+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    log2.write(id_equipo+' ['+fecha+' '+hour+']'+" Inicia Grabación CAM"+num_cam+'   IP: 10.1.1.'+num_ip+'\n\n') 
    log2.close()
    ###################################################################################
    tiempo_inicial = time.time() # guarda el tiempo de inicio
    

    # ejecuta la consola con el comando ffmpeg
    os.system('ffmpeg -t '+tiempo_grabacion_videos+' -i rtsp://admin:xiriox3000@10.1.1.'+num_ip+':554 -acodec copy -vcodec copy '+FILE_OUTPUT+' > /home/xirioxinf/Documentos/descarte_xiriox/grabar/output/output'+num_cam+'.csv 2>&1')
    """proc = subprocess.Popen(['ffmpeg -t '+tiempo_grabacion_videos+' -i rtsp://admin:xiriox3000@10.1.1.'+num_ip+':554 -acodec copy -vcodec copy '+FILE_OUTPUT+' > /home/xirioxinf/Documentos/descarte_xiriox/grabar/output/output'+num_cam+'.csv 2>&1'], shell=True)
    pid = proc.pid
    print(pid, num_ip, num_cam)"""
    tiempo_final = time.time() # guerda el tiempo final
    tiempo_ejecucion = tiempo_final - tiempo_inicial # guerda el tiempo total de ejecución
    """tiem = open ('tiempos.txt','a') #crea el archivo log
    tiem.write("tiempo total cam"+num_cam+"   "+str(tiempo_ejecucion)+'\n') 
    tiem.close() """
    time.sleep(10)
    ###################################################################################
    ### LOG MÓDULO PARA ERROR
    if (tiempo_ejecucion) < tiempo_minimo_error:
        log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
        log.write(id_equipo+' ['+fecha+' '+time.strftime('%H:%M:%S')+']'+" Error CAM"+num_cam+'   IP: 10.1.1.'+num_ip+" - No logra comunicar con la cámara"+'\n\n') 
        log.close()
        log2 = open (dir_videos+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
        log2.write(id_equipo+' ['+fecha+' '+time.strftime('%H:%M:%S')+']'+" Error CAM"+num_cam+'   IP: 10.1.1.'+num_ip+" - No logra comunicar con la cámara"+'\n\n') 
        log2.close()
    ###################################################################################
    ### LOG FINALIZA GRABACIÓN
    log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    log.write(id_equipo+' ['+fecha+' '+time.strftime('%H:%M:%S')+']'+" Finaliza Grabación CAM"+num_cam+'   IP: 10.1.1.'+num_ip+'\n\n') 
    log.close()
    ### LOG FINALIZA GRABACIÓN
    log2 = open (dir_videos+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    log2.write(id_equipo+' ['+fecha+' '+time.strftime('%H:%M:%S')+']'+" Finaliza Grabación CAM"+num_cam+'   IP: 10.1.1.'+num_ip+'\n\n') 
    log2.close()
    ###################################################################################

#urls = [70,71,73,72,74,75,76,77,78,79,80,81,82,83,84,85] # número para cada cámara en la conexión RTSP
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

main()


