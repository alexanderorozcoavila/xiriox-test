# -*- coding: utf-8 -*-
#!/usr/bin/python
########################################################################
# Encripta el video de la cámara que se recibe por parámetro en tiempo real
# mientras se está grabando
########################################################################
import time
import os
import hashlib
import threading
import configparser
import cron
import sys
#sys.path.insert(0, '/home/xirioxinf/Documentos/descarte_xiriox')
import hdd_sch
from tkinter import *
#%Y - Numero de año entero (2014)
#%m - Mes en número
#%d - Día del mes

"""flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','r') #crea el archivo log
estado_encriptar = flag.read()
flag.close()
if estado_encriptar == '2':
    sys.exit()"""
print('Iniciando Encriptar')
time.sleep(5)
cantDiscos = 2

externalHdd = ['Ext1', 'Ext2', 'Ext3']
porcen = hdd_sch.porcentajes(externalHdd)
print(porcen)
if porcen == 'ERROR':
    hddFolder = os.listdir('/media/xirioxinf/')
    if len(hddFolder) <= cantDiscos:    
        discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
        discoLleno.write('true')
        discoLleno.close()
    else:
        discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/discoLleno.txt', 'w')
        discoLleno.write('true')
        discoLleno.close()
    configuracion = configparser.ConfigParser() # abre archivo de configuración
    configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración

    configuracion['Directorios']['dir_encrypt'] = '/media/xirioxinf/'+porcen
    #configuracion['Directorios']['dir_encrypt'] = '/media/xirioxinf/'+porcen
    with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
        configuracion.write(configfile)
    time.sleep(1)
    # crea y muestra la ventana de carga del software
    ventana = Tk()
    ventana.title("Error")
    ventana.geometry("400x240")
    if len(hddFolder) <= cantDiscos:
        imagen = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/error_discos.png")
    else:
        imagen = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/discos_llenos.png")
    fondo = Label(ventana,image=imagen).place(x=-1,y=-1)
    ventana.wm_attributes('-type', 'splash')
    ventana.mainloop()
else:
    discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/discoLleno.txt', 'w')
    discoLleno.write('false')
    discoLleno.close()
configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración

configuracion['Directorios']['dir_encrypt'] = '/media/xirioxinf/'+porcen
#configuracion['Directorios']['dir_encrypt'] = '/media/xirioxinf/'+porcen
with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
    configuracion.write(configfile)

configuracion = configparser.ConfigParser() # abre archivo de configuración
cam_conectadas = configparser.ConfigParser()
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
dir_videos = configuracion['Directorios']['dir_videos'] # lee el directorio de videos
#nombre_usuario = os.getlogin()
#dir_videos = "/media/"+nombre_usuario+"/Videos/CAM"
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos
cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema
id_equipo = configuracion['ID']['id_dri'] # id_equipo
#print(os.listdir("/media/"+nombre_usuario+"/"))

# Detecta el último video que se está grabando dentro de la carpeta de la cámara
def ultimo_video(num, fecha):
    lista = [] # Lista vacia para agregar elementos
    #print(dir_videos+'/'+fecha+'/CAM'+num+'/')
    files = os.listdir(dir_videos+'/'+fecha+'/CAM'+num+'/') # Obtiene todos los archivos del directorio de la cámara
    #print("FILES: ", files)
    #print(files) # imprime la url el directorio obtenido
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
    #print(lista) # Imprime la lista con los ficheros obtenidos
    lista.sort(reverse=True) # Ordena la lista de mayor a menor obteniendo el último archivo al principio de la lista
    #print("con sort: "+str(lista)) #Imprime la lista ordenada de mayor a menor
    #print("Último archivo grabado: "+ str(lista[0])) # Imprime el último archivo que se está grabando
    print(lista)
    return lista[0] # Retorna el primer elemento de la lista ordenada, el cual sería el último archivo grabado

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

# Encripta el último archivo que se está grabando de la cámara pasada por parámetro
# cambiando la secuencia binaria 'xf' por 'xiriox_solutions' a lo largo de todo el archivo
def encriptar_video(nombre_cam, num):

    configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
    #dir_videos = configuracion['Directorios']['dir_videos'] # lee el directorio de videos
    #dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el dir
    flag = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptar'+nombre_cam,'r+') #crea el archivo log
    flag_camara_state = flag.read()
    flag.close()
    if flag_camara_state == 'true':
        sys.exit()
    contador_sub = 1
    #print("DENTRO DE ", str(nombre_cam))
    seg = 0
    minu = 0    
    print ("Dentro de {0}".format(nombre_cam))
    fecha = time.strftime('%Y-%m-%d') # obtiene la fecha día/mes/año
    hora =  time.strftime('%H:%M:%S') # obtiene la hora hora/minutos/segundos
    ult_video = ultimo_video(num, fecha) # obtiene el último archivo que se está grabado (el actual)
    nombre_ult_video = ult_video.split(".")[0] # guarda el nombre del último video sin la extensión ".mp4"
    # abre (si no existe lo crea) un archivo para guardar el binario del video
    # en el directorio especificado por fecha y nombre de la cámara
    path = dir_encrypt+'/'+fecha+'/CAM'+num+'/'
    path2 = dir_videos+'/'+fecha+'/CAM'+num+'/'
    #print(path) # imprime el directorio especificado
    os.makedirs(path, exist_ok=True) # crea ese nuevo directorio, si existe no pasa nada
    os.makedirs(path2, exist_ok=True) # crea ese nuevo directorio, si existe no pasa nada
    log = open (dir_encrypt+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    log.write(id_equipo+' ['+fecha+' '+hora+']'+" Inicia encriptación CAM"+num+'\n\n') 
    log.close()

    log2 = open (dir_videos+'/'+fecha+'/log-'+fecha+'.txt','a') #crea el archivo log
    log2.write(id_equipo+' ['+fecha+' '+hora+']'+" Inicia encriptación CAM"+num+'\n\n')
    log2.close()

    # abre el video que se está grabando en modo lectura binaria
    f = open (dir_videos+'/'+fecha+'/CAM'+num+'/'+ult_video,'r+b')
    # abre un nuevo archivo para guardar los datos del video encriptados
    f2 = open(path+nombre_ult_video+".encrypt", "a+b")
    temp = -1 # variable temporal para ir guardando el tamaño del archivo encriptado
              # se inicia en -1 para no generar conflicto con el tamaño del archivo
    
    #ciclo para copiar cada 100000000bytes (100mb) desde el video al archivo en tiempo real
    flag_camaras = ''
    cambio_segundo = time.strftime('%S')
    minu = 0
    seg = 0
    minu2 = 0
    seg2 = 1
    contadorEncrypt = 0
    while (True):
        flag = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptar'+nombre_cam,'r') #crea el archivo log
        estado_encriptar = flag.read()
        flag.close()
        if estado_encriptar == 'true':
            print('SE DEBE SALIR DEL PROCESO DE ', str(nombre_cam))
            sys.exit()
        """configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
        dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos
        with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
            configuracion.write(configfile)"""
        fecha_aux = time.strftime('%Y-%m-%d') # obtiene la fecha día/mes/año 
        try:
            cam_conectadas.read('/home/xirioxinf/Documentos/descarte_xiriox/csv/cam_conectadas.ini')
        except Exception as e:
            print(e)
            pass
        cambio_segundo_aux = cambio_segundo
        cambio_segundo = time.strftime('%S')
        #print("1  "+cambio_segundo)
        #print("2  "+  cambio_segundo_aux)
        if cambio_segundo != cambio_segundo_aux:
            try:
                flag_camaras = cam_conectadas['CAM'][nombre_cam]
                print(flag_camaras)
            except Exception as e:
                print(e)
                pass
            if flag_camaras == 'false':
                #print("Cerrar cámara: "+nombre_cam)
                break
            else:
                print("Abrir cámara: "+nombre_cam)
                ult_video_aux = ultimo_video(num, fecha) # obtiene el último archivo que se está grabado (el actual)
                #time.sleep(0.1) # espera de 7 segundos para copiar la cantidad de bytes determinada
                #print(ult_video_aux)
                # variables con el tamaño de ambos archivos para ir comparándolos
                size1 = os.path.getsize(dir_videos+'/'+fecha+'/CAM'+num+'/'+ult_video)
                size2 = os.path.getsize(path+nombre_ult_video+".encrypt")
                #print(path+nombre_ult_video)
                
                temp = size2 # asigna el tamaño que lleva hasta el momento el archivo encriptado
                mensaje = f.read(1000000) # lee 100mb desde el archivo de video que se está grabando
                if contadorEncrypt < 1:
                    print("REEMPLAZA")
                    mensaje = mensaje.replace(b'xf', b'xiriox_solutions') # modifica el binario del archivo de video encriptándolo
                    contadorEncrypt = contadorEncrypt+1
                f2.write(mensaje) # se escriben los datos encriptados en el nuevo archivo
                #se compara el tamaño de los archivos para terminar el proceso
                if size2 >= size1:
                    #print("Dentro size")
                    if ult_video == ult_video_aux:
                        flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','r') #crea el archivo log
                        estado_encriptar = flag.read()
                        flag.close()
                        
                        print(estado_encriptar)
                        if estado_encriptar == '2':
                            print("Termina por apagado")
                            flag = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptar'+nombre_cam,'w+') #crea el archivo log
                            flag.write('true')
                            flag.close()
                            break
                        #print("Dentro ultimo_video")
                        # verifica si la fecha es distinta a la actual y si el directorio de la fecha actual existe
                        if fecha != fecha_aux and os.path.isdir(dir_videos+'/'+fecha_aux):
                            print("Termina por fecha "+ nombre_cam)
                            time.sleep(5)
                            break
                    else:
                        # si el último video que se está grabando es diferente al que se está encriptando
                        print("Termina por cambio de video " + nombre_cam)
                        #time.sleep(5)
                        break
                try:
                    direct = dir_encrypt+"/"+fecha+'/metadata/METADATA.csv'
                    meta = open(direct,"r")
                    gps = meta.readlines()[-1]
                    meta.close()
                    gps = gps.split(",     ")
                    #print(gps)
                except Exception as e:
                    gps = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']
                    #print(gps)
                #Se guarda el .srt en la carpeta encrypt
                sub = open(path+nombre_ult_video+".srt", "a")
                minu, seg, seg_str, min_str, minu2, seg2, min_str2, seg_str2 = cron.min_seg(minu, seg, minu2, seg2)
                sub.write(
                    str(contador_sub)+'\n'+
                    '00:'+min_str+seg_str+' --> '+ '00:'+min_str2+seg_str2+'\n'+
                    gps[0]+'\n'+
                    gps[1]+'\n'+
                    gps[2]+'\n'+
                    gps[3]+'\n'+
                    gps[4]+'\n'+
                    gps[5]+'\n'+
                    gps[6]+'\n\n'
                    )
                contador_sub = contador_sub+1
                #print(contador_sub)
    print("SALE")
    f.close() # cierra el archivo 1
    f2.close() # cierra el archivo 2
    
    ########################################################################
    # Como el video que se estaba grabando aún no finalizaba, el encabezado del 
    # archivo encriptado queda corrupto, por lo tanto una vez el archivo se ha cerrado
    # correctamente se procede a la copia de un encabezado de 100kb del inicio y se pegan 
    # en el archivo encriptado dejando el fichero sin errores
    ########################################################################
    #   Se abren de nuevo los archivos para reparar el encabezado
    f = open (dir_videos+'/'+fecha+'/CAM'+num+'/'+ult_video,'r+b')
    info1 = f.read(100) # se copian los 100kb
    f.close() # cierra el archivo
    # abre nuevamente el archivo encriptado desde el comienzo 
    f2 = open(path+nombre_ult_video+".encrypt", "r+b")
    f2.write(info1) # copia los 100kb al inicio del fichero
    f2.close() # cierra el archivo 

    os.makedirs(path+'/md5', exist_ok=True) # crea ese nuevo directorio, si existe no pasa nada
    # genera un archivo md5 del archivo y directorio pasados por parámetro (descomentar la línea de abajo)
    hasher_md5(dir_videos+'/'+fecha+'/CAM'+num+'/'+ult_video, path+'md5/'+nombre_ult_video+".md5.txt")
    try:
        os.system('sudo cp '+path+nombre_ult_video+".srt "+path2+nombre_ult_video+".srt")
    except Exception as e:
        print(e)

    print("SALE 2")
    

for i in range(0,int(cantidad_camaras)):
    print("TRUE")
    hilo = threading.Thread(name='Hilo{}'.format(i), target=encriptar_video, args=('CAM'+str(i+1), str(i+1),))
    hilo.start()

                
