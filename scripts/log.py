import configparser, time, sys, os

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración

dir_videos = configuracion['Directorios']['dir_videos'] # lee el directorio de videos
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos

evento = str(sys.argv[1])
id_equipo = configuracion['ID']['id_dri'] # id_equipo
id_embarcacion = configuracion['ID']['id_embarcacion'] # id_equipo
fecha = time.strftime('%Y-%m-%d') # se obtiene la fecha
hora =  time.strftime('%H-%M-%S') # se obtiene la hora
hour =  time.strftime('%H:%M:%S') # se obtiene la hora

path = dir_videos+'/'+fecha+'/'
path_encrypt = dir_encrypt+'/'+fecha+'/'

os.makedirs(path, exist_ok=True) # crea el directorio, si ya existe no hace nada
os.makedirs(path_encrypt, exist_ok=True) # crea el directorio, si ya existe no hace nada

log = open (dir_videos+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
log.write(id_equipo+' '+id_embarcacion+' ['+fecha+' '+time.strftime('%H:%M:%S')+'] '+evento+'\n\n') 
log.close()

log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
log.write(id_equipo+' '+id_embarcacion+' ['+fecha+' '+time.strftime('%H:%M:%S')+'] '+evento+'\n\n') 
log.close()