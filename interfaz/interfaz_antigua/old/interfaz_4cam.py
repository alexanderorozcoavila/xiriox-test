#!/usr/bin/env python
import numpy as np
import cv2
import os
import time
import uuid
from PIL import ImageFont, ImageDraw, Image
import threading
import psutil
import configparser

direc_principal = '/home/xirioxinf/Documentos'
configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos
cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema
version = "v"+configuracion['Version']['version']

cam_conectadas = configparser.ConfigParser() # abre archivo de configuración
cam_conectadas['CAM'] = {   'CAM1': 'false',
                            'CAM2': 'false',
                            'CAM3': 'false',
                            'CAM4': 'false',}
with open(direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
    cam_conectadas.write(configfile)

ttf = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', 21) # Tipo de font y tamaño para los textos en pantalla
##############################################
myuuid = configuracion['ID']['id_dri']
##############################################
x = 810 # ancho de las imágenes de las cámaras para visualizar
y = 540 # alto de las imágenes de las cámaras para visualizar
##############################################
print("-- INICIANDO SISTEMA --")
##############################################
arr_frames = [] # Array que contiene las matrices de los frames para todas las cámaras
arr_ret = [] # Array que contiene los flag para reconocer si se obtuvo el frame de forma exitosa
#Se inicia el soporte para 4 cámaras 
for i in range(0,4): # se inicializan ambos array (el rango de 0 a 4 debe ser fijo)
    arr_frames.append(Image.new("RGB", (x,y), (25, 0, 51))) # crea imágenes en negro para cada cámara
    ImageDraw.Draw(arr_frames[i]).text((10,20), "Conectando CAM "+str(i+1), fill='white', font=ttf) # Crea un texto de "conectando" para cada cámara
    arr_ret.append(True) # inicializa todas las cámaras en True
#print(arr_frames)
##############################################
#frame = cv2.imread("/home/xirioxinf/Documentos/logo.jpg")
name = "Descarte de Pesca Xiriox" # nombre de la ventana principal

#cv2.imshow(name,frame)
##############################################
# se crea la ventana y se coloca en modo pantalla completa
cv2.namedWindow(name, cv2.WND_PROP_FULLSCREEN); 
cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

urls = [] # número para cada cámara en la conexión RTSP
for i in range(0,int(cantidad_camaras)):
    urls.append(configuracion['IP']['cam'+str(i+1)])

print(urls)

def guardarFpsBitrate(fps, bitrate, resolucion, num):
    archivo = open(direc_principal+'/descarte_xiriox/metadatos/info/info_cam'+num,'w')
    archivo.write(fps+"fps - "+bitrate+" - "+resolucion)
    archivo.close()

def connectionCam(var, var2):
    while True:

        print("Conectando Cámara antes: ", str(var2+1))
        respuesta = os.system("ping -c 1 10.1.1."+var)
        print("Respuesta del ping: ", respuesta)
        #print(u"\u001b[33m"+str(respuesta))
        if respuesta == 0:
            cap1 = cv2.VideoCapture("rtsp://admin:xiriox3000@10.1.1."+var+":554") # crea la conexión con la cámara
            print(cap1.isOpened()) # indica la conexión es exitosa devuelve true
            count = 0
            fps = 0
            while True: # ciclo para ir recibiendo los frames
                seg =  time.strftime('%S') # se obtiene el segundo actual
                ret, ret_frame = cap1.read() # ret -> indica si el frame es recibido de forma correcta, ret_frame -> contenido del frame

                if ret: # si es recibido de forma correcta se redimensiona el frame
                    try:
                        bitrate_file = open(direc_principal+'/descarte_xiriox/grabar/output/output'+str(var2+1)+'.csv', 'r')
                        bitrate = bitrate_file.readlines()[-1]
                        bitrate_file.close()
                        bitrate = bitrate.split(" ")
                        while "" in bitrate:
                            bitrate.remove("")
                        for i in range(0,len(bitrate)):
                            if "kbits/s" in bitrate[i]:
                                bitrate_cam = bitrate[i]
                                if "bitrate=" in bitrate_cam:
                                    bitrate_cam = bitrate_cam.replace("bitrate=","")
                                else:
                                    pass
                                break
                            else:
                                bitrate_cam = "--kbits/s"

                    except Exception as e:
                        bitrate_cam = "--kbits/s"

                    w = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
                    h = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    #print(w, h)

                    arr_frames[var2] = cv2.resize(ret_frame, (x, y)) # redimensiona el frame

                    cv2.putText(arr_frames[var2], "CAM "+str(var2+1)+" 10.1.1."+var+"  - FPS: "+str(fps)+'    '+bitrate_cam+'    '+str(w)+'x'+str(h), (6, 21), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,0), 1,lineType=cv2.LINE_AA)
                    cv2.putText(arr_frames[var2], "CAM "+str(var2+1)+" 10.1.1."+var+"  - FPS: "+str(fps)+'    '+bitrate_cam+'    '+str(w)+'x'+str(h), (5, 20), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255,255,255), 1,lineType=cv2.LINE_AA)
                    
                    cam_conectadas.set('CAM', 'CAM'+str(var2+1), 'true') # indica que la cámara está conectada y recibe la señal
                    with open(direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
                        cam_conectadas.write(configfile) # escribe en el archivo ini que la cámara está funcionando
                    count = count+1 # cuenta un fps

                    if time.strftime('%S') != seg:
                        if count>15:
                            count = 15
                        fps = count
                        guardarFpsBitrate(str(fps), str(bitrate_cam), str(w)+'x'+str(h), str(var2+1))
                        count = 0
                    else:
                        guardarFpsBitrate(str(fps), str(bitrate_cam), str(w)+'x'+str(h), str(var2+1))

                else:
                    cam_conectadas.set('CAM', 'CAM'+str(var2+1), 'false')
                    with open(direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
                        cam_conectadas.write(configfile)

                    cap1 = cv2.VideoCapture("rtsp://admin:xiriox3000@10.1.1."+var+":554") # intenta reconectar con la cámara
                    arr_frames[var2] = Image.new("RGB", (x,y), (25, 0, 51)) # crea una imágen de fondo negro
                    ImageDraw.Draw(arr_frames[var2]).text((10,20), '-Offline CAM '+str(var2+1)+'    10.1.1.'+var, fill='white', font=ttf) # escribe texto Offline
                    break

        time.sleep(4)    

def principal():
    for i in range(0,int(cantidad_camaras)): # ciclo para los hilos
        t = threading.Thread(target=connectionCam, args = (str(urls[i]), i)) # crea el hilo
        t.start() # corre el hilo

    gps = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']
    gps_aux = gps
    while True:
        #print("activo principal")
        #print(arr_frames)
        fecha = time.strftime('%d-%m-%Y')
        fecha2 = time.strftime('%Y-%m-%d')
        hora =  time.strftime('%H:%M:%S')
        #img = np.zeros((512,512,3), np.uint8)
        #img = cv2.resize(img, (300, y))
        # recuadro (0,0) que contiene la información de navegación
        #gps_aux = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']
        try:
            direct = dir_encrypt+"/"+fecha2+'/metadata/metada_temp.csv'
            f = open(direct,"r")
            #gps = f.readlines()[-1]
            gps = f.read()
            f.close()
            gps = gps.split(",     ")
            #gps_aux = gps
            #print(gps)
            if len(gps) == 1:
                #gps = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']
                gps = gps_aux
                #print(gps)
            else:
                gps_aux = gps
        except Exception as e:
            #gps = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']
            gps = gps_aux
            print(e)

        #print(gps)
        #print(len(gps))
        
        img_vacia = Image.new("RGB", (300,y), (25, 0, 51))
        img = Image.new("RGB", (300,y), (25, 0, 51))
        ImageDraw.Draw(img).text((10,20), fecha+" "+hora, fill='white', font=ttf)
        ImageDraw.Draw(img).text((10,45), "ID: "+str(myuuid), fill='white', font=ttf)
        #ImageDraw.Draw(img).text((10,70), "LAT: 00° 00,00'", fill='white', font=ttf)
        ImageDraw.Draw(img).text((10,70), "LAT: "+gps[3], fill='white', font=ttf)
        ImageDraw.Draw(img).text((10,95), "LON: "+gps[4], fill='white', font=ttf)
        ImageDraw.Draw(img).text((10,120), "RUMBO: "+gps[6], fill='white', font=ttf)
        ImageDraw.Draw(img).text((10,145), "VEL (NUDOS): "+gps[5], fill='white', font=ttf)
        # recuadro (0,4) que muestra la información de los discos duros
        img2 = Image.new("RGB", (300,y), (25, 0, 51))
        logo_xiriox = Image.open(direc_principal+"/descarte_xiriox/interfaz/img/Recurso 1.png") # carga el logo de xiriox
        img2.paste(logo_xiriox, (40,y-120), logo_xiriox) # pega la imágen sobre el background creado anteriormente (img2)
        ImageDraw.Draw(img2).text((80,y-150), "Oraculus 4000", fill='white', font=ttf)
        ###########################################################################
        flag_grabacion = open(direc_principal+"/descarte_xiriox/grabar/grabar", "r")
        fg = flag_grabacion.read()
        flag_grabacion.close()
        if fg == '1':
            ImageDraw.Draw(img2).text((10,20), "GRABANDO", fill='white', font=ttf)
        else:
            if fg == '2':
                #ImageDraw.Draw(img2).text((10,20), "GRABANDO", fill='white', font=ttf)
                ImageDraw.Draw(img2).text((10,20), "APAGANDO", fill='white', font=ttf)
            else:
                #ImageDraw.Draw(img2).text((10,20), "GRABANDO", fill='white', font=ttf)
                ImageDraw.Draw(img2).text((10,20), "DETENIDO", fill='white', font=ttf)
        ###########################################################################
        configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración

        try:
            disco_duro = psutil.disk_usage('/media/xirioxinf/Ext1')#cambiar directorio para detección de disco
            espacioDisponible = disco_duro[3] #Mostrar espacio libre en GB
        except Exception as e:
            espacioDisponible = 0
            print(e)
        try:
            disco_duro2 = psutil.disk_usage('/media/xirioxinf/Ext2')#cambiar directorio para detección de disco
            espacioDisponible2 = disco_duro[3] #Mostrar espacio libre en GB
        except Exception as e:
            espacioDisponible2 = 0
            print(e)

        """try:
            disco_duro2 = psutil.disk_usage('/media/xirioxinf/Ext2')#cambiar directorio para detección de disco  
            espacioDisponible2 = str(disco_duro2[3])+'% HDD Ext2 Ocupado' #Mostrar espacio libre en GB
        except Exception as e:
            espacioDisponible2 = 'ERROR DISCO EXTERNO 2'"""

        arrayAlarmas = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/nombresAlarmas.txt', 'r+')
        dataa = arrayAlarmas.read()
        arrayAlarmas.close()

        try:
            ImageDraw.Draw(img2).text((10,45), str((espacioDisponible*0.5+espacioDisponible2*0.5))+" % HDD Ocupado", fill='white', font=ttf)
        except Exception as e:
            ImageDraw.Draw(img2).text((10,45), "ERROR Disco duro externo", fill='white', font=ttf)
        
        if dataa == "":
            img_boton = Image.open("/home/xirioxinf/Documentos/descarte_xiriox/interfaz/img/boton_verde.png")
            img.paste(img_boton, (10,500), img_boton) # pega la imágen sobre el background creado anteriormente (img2)
            ImageDraw.Draw(img).text((60,510), "OK", fill='white', font=ttf)
        else:
            img_boton = Image.open("/home/xirioxinf/Documentos/descarte_xiriox/interfaz/img/boton_azul.png")
            #img = img.convert("BGR")
            #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img.paste(img_boton, (10,500), img_boton) # pega la imágen sobre el background creado anteriormente (img2)
            ImageDraw.Draw(img).text((60,510), "ALARMA", fill='white', font=ttf)
        #ImageDraw.Draw(img2).text((10,75), espacioDisponible2, fill='white', font=ttf)

        ImageDraw.Draw(img2).text((10,130), dataa, fill='white', font=ttf)
        ImageDraw.Draw(img2).text((10,y-30), version+"      www.xiriox.com", fill='white', font=ttf)
        #cv2.putText(img, "ID: "+str(myuuid), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,lineType=cv2.LINE_AA)
        #cv2.putText(img,fecha+" "+hora, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,lineType=cv2.LINE_AA)
        #im = np.concatenate((im1, im5), axis=0)

        horizontal1 = np.concatenate((img, arr_frames[0], arr_frames[1]), axis=1)
        horizontal2 = np.concatenate((img2, arr_frames[2], arr_frames[3]), axis=1)
        #horizontal1 = cv2.hconcat([im1, im2, im3])
        #horizontal2 = cv2.hconcat([im4, im5, im6])
        """horizontal3 = np.concatenate((img_vacia, arr_frames[8], arr_frames[9], arr_frames[10], arr_frames[11]), axis=1)
        horizontal4 = np.concatenate((img2, arr_frames[12], arr_frames[13], arr_frames[14], arr_frames[15]), axis=1)"""

        #vertical1 = np.concatenate((horizontal1,horizontal2), axis=0)
        #vertical2 = np.concatenate((horizontal3,horizontal4), axis=0)

        total = np.concatenate((horizontal1,horizontal2), axis=0) # se juntan todos los frames en una sola ventana

        # Display the resulting frame
        cv2.imshow(name,total) # se muestra toda la ventana
        #else:
            #break
        #gps_aux = gps
        if cv2.waitKey(1) & 0xFF == ord('q'): # se espera presionar la letra "q" para cerrar la ventana
            pass

principal() # se ejecuta la función principal

print(arr_frames)
