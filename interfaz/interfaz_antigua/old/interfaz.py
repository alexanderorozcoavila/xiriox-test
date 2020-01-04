#!/usr/bin/env python
import cv2
import numpy as np
import os
import time
import uuid
from PIL import ImageFont, ImageDraw, Image
import threading
import psutil
import configparser

direc_principal = '/home/xirioxinf/Documentos'
#direc_principal = '/home/omvega/Documents/DESCARTE_FINAL_SICAL'

#direc_encriptado = '/media/xirioxinf/Encrypt/'
#direc_encriptado = "/media/omvega/W7AIO/"
configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos

cam_conectadas = configparser.ConfigParser() # abre archivo de configuración
cam_conectadas['CAM'] = {    'CAM1': 'true',
                            'CAM2': 'true',
                            'CAM3': 'true',
                            'CAM4': 'true',
                            'CAM5': 'true',
                            'CAM6': 'true',
                            'CAM7': 'true',
                            'CAM8': 'true',
                            'CAM9': 'true',
                            'CAM10': 'true',
                            'CAM11': 'true',
                            'CAM12': 'true',
                            'CAM13': 'true',
                            'CAM14': 'true',
                            'CAM15': 'true',
                            'CAM16': 'true',}
with open(direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
    cam_conectadas.write(configfile)

ttf = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', 20) # Tipo de font y tamaño para los textos en pantalla
##############################################
myuuid = configuracion['ID']['id_dri']
##############################################
x = 405 # ancho de las imágenes de las cámaras para visualizar
y = 270 # alto de las imágenes de las cámaras para visualizar
##############################################
print("-- INICIANDO SISTEMA --")
##############################################
arr_frames = [] # Array que contiene las matrices de los frames para todas las cámaras
arr_ret = [] # Array que contiene los flag para reconocer si se obtuvo el frame de forma exitosa
for i in range(0,16): # se inicializan ambos array
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

urls = [70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85] # número para cada cámara en la conexión RTSP

def guardarFpsBitrate(fps, bitrate, resolucion, num):
    archivo = open(direc_principal+'/descarte_xiriox/metadatos/info/info_cam'+num,'w')
    archivo.write(fps+"fps - "+bitrate+" - "+resolucion)
    archivo.close()
    """archivo = open('../metadatos/info/bitrate_cam'+num,'w')
    archivo.write(bitrate)
    archivo.close()"""

def connectionCam(var, var2):
    
        cap1 = cv2.VideoCapture("rtsp://admin:xiriox3000@10.1.1."+var+":554") # crea la conexión con la cámara
        print(cap1.isOpened()) # indica la conexión es exitosa devuelve true
        count = 0
        fps = 0
        while True: # ciclo para ir recibiendo los frames
            seg =  time.strftime('%S') # se obtiene el segundo actual
            ret, ret_frame = cap1.read() # ret -> indica si el frame es recibido de forma correcta, ret_frame -> contenido del frame
            #print(arr_ret, arr_frames)
            #if int(var) < 6:
            if ret: # si es recibido de forma correcta se redimensiona el frame
                try:
                    bitrate_file = open(direc_principal+'/descarte_xiriox/grabar/output/output'+str(var2+1)+'.csv', 'r')
                    bitrate = bitrate_file.readlines()[-1]
                    bitrate_file.close()
                    bitrate = bitrate.split(" ")
                    #print(bitrate)
                    #print(bitrate.index('fps'))
                    while "" in bitrate:
                        bitrate.remove("")
                    for i in range(0,len(bitrate)):
                        if "kbits/s" in bitrate[i]:
                            #print(bitrate[i])
                            bitrate_cam = bitrate[i]
                            if "bitrate=" in bitrate_cam:
                                #print(bitrate_cam)
                                bitrate_cam = bitrate_cam.replace("bitrate=","")
                                #print("ESTÄ")
                                #print(bitrate_cam)
                            else:
                                pass
                            break
                        else:
                            bitrate_cam = "--kbits/s"


                except Exception as e:
                    bitrate_cam = "--kbits/s"

                """bit_num = bitrate_cam.replace('kbits/s', '')
                print(bit_num)
                bitrate_cam = bit_num

                if bitrate_cam != '--':
                    if float(bitrate_cam) < 1024:
                        bitrate_cam = 1024

                    bitrate_cam = str(bitrate_cam)
                #print(len(bitrate))"""

                w = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
                #print(w, h)

                arr_frames[var2] = cv2.resize(ret_frame, (x, y)) # redimensiona el frame

                cv2.putText(arr_frames[var2], "FPS: "+str(fps)+'    '+bitrate_cam+'    '+str(w)+'x'+str(h), (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1,lineType=cv2.LINE_AA)
                cv2.putText(arr_frames[var2], "FPS: "+str(fps)+'    '+bitrate_cam+'    '+str(w)+'x'+str(h), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,lineType=cv2.LINE_AA)
                
                cam_conectadas.set('CAM', 'CAM'+str(var2+1), 'true') # indica que la cámara está conectada y recibe la señal
                with open(direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
                    cam_conectadas.write(configfile) # escribe en el archivo ini que la cámara está funcionando
                count = count+1 # cuenta un fps

                if time.strftime('%S') != seg:
                    if count>15:
                        count = 15
                    fps = count
                    #cv2.putText(arr_frames[var2], "FPS: "+str(fps)+'    '+bitrate_cam+'kbits/s    '+str(w)+'x'+str(h), (7, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1,lineType=cv2.LINE_AA)
                    #cv2.putText(arr_frames[var2], "FPS: "+str(fps)+'    '+bitrate_cam+'kbits/s    '+str(w)+'x'+str(h), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,lineType=cv2.LINE_AA)
                    guardarFpsBitrate(str(fps), str(bitrate_cam), str(w)+'x'+str(h), str(var2+1))
                    count = 0
                else:
                    #cv2.putText(arr_frames[var2], "FPS: "+str(fps)+'    '+bitrate_cam+'kbits/s    '+str(w)+'x'+str(h), (7, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1,lineType=cv2.LINE_AA)
                    #cv2.putText(arr_frames[var2], "FPS: "+str(fps)+'    '+bitrate_cam+'kbits/s    '+str(w)+'x'+str(h), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,lineType=cv2.LINE_AA)
                    guardarFpsBitrate(str(fps), str(bitrate_cam), str(w)+'x'+str(h), str(var2+1))

                #print('output'+str(var2+1)+'txt')
                
                #print(bitrate[8])
                #cv2.putText(arr_frames[var2], bitrate[8], (300, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,lineType=cv2.LINE_AA)


            else:
                cam_conectadas.set('CAM', 'CAM'+str(var2+1), 'false')
                with open(direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
                    cam_conectadas.write(configfile)

                #time.sleep(15)
                #if int(var) < 6:
                cap1 = cv2.VideoCapture("rtsp://admin:xiriox3000@10.1.1."+var+":554") # intenta reconectar con la cámara
                arr_frames[var2] = Image.new("RGB", (x,y), (25, 0, 51)) # crea una imágen de fondo negro
                ImageDraw.Draw(arr_frames[var2]).text((10,20), '-Offline CAM '+str(var2+1)+'    10.1.1.'+var, fill='white', font=ttf) # escribe texto Offline
        

def principal():
    for i in range(0,6): # ciclo para los hilos
        t = threading.Thread(target=connectionCam, args = (str(urls[i]), i)) # crea el hilo
        t.start() # corre el hilo

    gps = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']
    while True:
        #print("activo principal")
        #print(arr_frames)
        fecha = time.strftime('%d-%m-%Y')
        fecha2 = time.strftime('%Y-%m-%d')
        hora =  time.strftime('%H:%M:%S')
        #img = np.zeros((512,512,3), np.uint8)
        #img = cv2.resize(img, (300, y))
        # recuadro (0,0) que contiene la información de navegación
        try:
            direct = dir_encrypt+"/"+fecha2+'/metadata/metada_temp.csv'
            f = open(direct,"r")
            #gps = f.readlines()[-1]
            gps = f.read()
            f.close()
            gps = gps.split(",     ")
            #print(gps)
            if len(gps) == 1:
                gps = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']
            #print(gps)
        except Exception as e:
            gps = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']

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
        img2.paste(logo_xiriox, (40,150), logo_xiriox) # pega la imágen sobre el background creado anteriormente (img2)
        ###########################################################################
        flag_grabacion = open(direc_principal+"/descarte_xiriox/grabar/grabar", "r")
        fg = flag_grabacion.read()
        flag_grabacion.close()
        if fg == '1':
            ImageDraw.Draw(img2).text((10,20), "GRABANDO", fill='white', font=ttf)
        else:
            if fg == '2':
                ImageDraw.Draw(img2).text((10,20), "APAGANDO", fill='white', font=ttf)
            else:
                ImageDraw.Draw(img2).text((10,20), "DETENIDO", fill='white', font=ttf)
        ###########################################################################
        disco_duro = psutil.disk_usage(dir_encrypt)#cambiar directorio para detección de disco 
        espacioDisponible = str(disco_duro[3])+'% HDD Ocupado' #Mostrar espacio libre en GB
        ImageDraw.Draw(img2).text((10,45), espacioDisponible, fill='white', font=ttf)
        ImageDraw.Draw(img2).text((70,240), "www.xiriox.com", fill='white', font=ttf)
        #cv2.putText(img, "ID: "+str(myuuid), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,lineType=cv2.LINE_AA)
        #cv2.putText(img,fecha+" "+hora, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,lineType=cv2.LINE_AA)
        #im = np.concatenate((im1, im5), axis=0)

        horizontal1 = np.concatenate((img, arr_frames[0], arr_frames[1], arr_frames[2], arr_frames[3]), axis=1)
        horizontal2 = np.concatenate((img_vacia, arr_frames[4], arr_frames[5], arr_frames[6], arr_frames[7]), axis=1)
        #horizontal1 = cv2.hconcat([im1, im2, im3])
        #horizontal2 = cv2.hconcat([im4, im5, im6])
        horizontal3 = np.concatenate((img_vacia, arr_frames[8], arr_frames[9], arr_frames[10], arr_frames[11]), axis=1)
        horizontal4 = np.concatenate((img2, arr_frames[12], arr_frames[13], arr_frames[14], arr_frames[15]), axis=1)

        vertical1 = np.concatenate((horizontal1,horizontal2), axis=0)
        vertical2 = np.concatenate((horizontal3,horizontal4), axis=0)

        total = np.concatenate((vertical1,vertical2), axis=0) # se juntan todos los frames en una sola ventana
        # Display the resulting frame
        cv2.imshow(name,total) # se muestra toda la ventana
        #else:
            #break
        #gps_aux = gps
        if cv2.waitKey(1) & 0xFF == ord('q'): # se espera presionar la letra "q" para cerrar la ventana
            break



#urls = [cap1,cap2,cap3,cap4,cap5,cap6,cap7,cap8,cap9,cap10,cap11,cap12,cap13,cap14,cap15,cap16]

""""""
#t = threading.Thread(target=principal, args = (123))
principal() # se ejecuta la función principal


#cv2.waitKey(15000)
#cv2.destroyAllWindows()
print(arr_frames)
