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

# Detecta el último video que se está grabando dentro de la carpeta de la cámara
def ultimo_video():
    lista = [] # Lista vacia para agregar elementos
    #print(dir_videos+'/'+fecha+'/CAM'+num+'/')
    #files = os.listdir(dir_videos+'/'+fecha+'/CAM'+num+'/') # Obtiene todos los archivos del directorio de la cámara
    files = os.listdir('/media/xirioxinf/Int1/2019-12-12/CAM1/') # Obtiene todos los archivos del directorio de la cámara
    print(files)
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
    print(lista[0])
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
    contador_sub = 1
    print("DENTRO")
    seg = 0
    minu = 0    
    print ("Dentro de {0}".format(nombre_cam))
    fecha = time.strftime('%Y-%m-%d') # obtiene la fecha día/mes/año
    hora =  time.strftime('%H:%M:%S') # obtiene la hora hora/minutos/segundos
    ult_video = ultimo_video() # obtiene el último archivo que se está grabado (el actual)
    nombre_ult_video = ult_video.split(".")[0] # guarda el nombre del último video sin la extensión ".mp4"
    # abre (si no existe lo crea) un archivo para guardar el binario del video
    # en el directorio especificado por fecha y nombre de la cámara
    #path = dir_encrypt+'/'+fecha+'/CAM'+num+'/'
    path2 = '/media/xirioxinf/Ext1/'
    #print(path) # imprime el directorio especificado

    # abre el video que se está grabando en modo lectura binaria
    f = open ('/media/xirioxinf/Int1/2019-12-12/CAM1/'+ult_video,'r+b')
    # abre un nuevo archivo para guardar los datos del video encriptados
    f2 = open(path2+nombre_ult_video+".encrypt", "a+b")
    temp = -1 # variable temporal para ir guardando el tamaño del archivo encriptado
              # se inicia en -1 para no generar conflicto con el tamaño del archivo
    estado_encriptar = 'false'
    #ciclo para copiar cada 100000000bytes (100mb) desde el video al archivo en tiempo real
    flag_camaras = ''
    cambio_segundo = time.strftime('%S')
    minu = 0
    seg = 0
    minu2 = 0
    seg2 = 1
    contadorEncrypt = 0
    while (True):
        if estado_encriptar == 'true':
            print('SE DEBE SALIR DEL PROCESO')
            sys.exit()

        fecha_aux = time.strftime('%Y-%m-%d') # obtiene la fecha día/mes/año 
        cambio_segundo_aux = cambio_segundo
        cambio_segundo = time.strftime('%S')
        if cambio_segundo != cambio_segundo_aux:
            try:
                flag_camaras = cam_conectadas['CAM'][nombre_cam]
            except Exception as e:
                pass
            if flag_camaras == 'false':
                break
            else:
                print("Abrir cámara: "+nombre_cam)
                ult_video_aux = ultimo_video() # obtiene el último archivo que se está grabado (el actual)
                #time.sleep(0.1) # espera de 7 segundos para copiar la cantidad de bytes determinada
                #print(ult_video_aux)
                # variables con el tamaño de ambos archivos para ir comparándolos
                size1 = os.path.getsize('/media/xirioxinf/Int1/2019-12-12/CAM1/'+ult_video)
                size2 = os.path.getsize(path2+nombre_ult_video+".encrypt")
                
                 # asigna el tamaño que lleva hasta el momento el archivo encriptado
                mensaje = f.read(10000000) # lee 100mb desde el archivo de video que se está grabando
                """if b'xf' in mensaje:
                    print("existe el valor")"""
                    #print(mensaje)
                if contadorEncrypt < 1:
                    print("REEMPLAZA")
                    mensaje = mensaje.replace(b'xf', b'xiriox_solutions') # modifica el binario del archivo de video encriptándolo
                    contadorEncrypt = contadorEncrypt+1
                f2.write(mensaje) # se escriben los datos encriptados en el nuevo archivo
                #se compara el tamaño de los archivos para terminar el proceso
                if size2 >= size1 or temp == size2:
                    print("Dentro size")
                    print(ult_video, ult_video_aux)
                    if ult_video == ult_video_aux:
                        if estado_encriptar == 'false':
                            print("Termina por apagado")
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
                temp = size2
                #print(contador_sub)

    f.close() # cierra el archivo 1
    f2.close() # cierra el archivo 2
    
    ########################################################################
    # Como el video que se estaba grabando aún no finalizaba, el encabezado del 
    # archivo encriptado queda corrupto, por lo tanto una vez el archivo se ha cerrado
    # correctamente se procede a la copia de un encabezado de 100kb del inicio y se pegan 
    # en el archivo encriptado dejando el fichero sin errores
    ########################################################################
    #   Se abren de nuevo los archivos para reparar el encabezado
    f = open ("/media/xirioxinf/Int1/2019-12-12/CAM1"+ult_video,'r+b')
    info1 = f.read(100) # se copian los 100kb
    f.close() # cierra el archivo
    # abre nuevamente el archivo encriptado desde el comienzo 
    f2 = open(path2+nombre_ult_video+".encrypt", "r+b")
    f2.write(info1) # copia los 100kb al inicio del fichero
    f2.close() # cierra el archivo 

    os.makedirs(path2+'/md5', exist_ok=True) # crea ese nuevo directorio, si existe no pasa nada
    # genera un archivo md5 del archivo y directorio pasados por parámetro (descomentar la línea de abajo)
    #hasher_md5(path2+nombre_ult_video+".md5.txt")
    """try:
                    os.system('sudo cp '+path+nombre_ult_video+".srt "+path2+nombre_ult_video+".srt")
                except Exception as e:
                    print(e)"""
    

for i in range(0,int(1)):
    print("TRUE")
    hilo = threading.Thread(name='Hilo{}'.format(i), target=encriptar_video, args=('CAM'+str(i+1), str(i+1),))
    hilo.start()


                
