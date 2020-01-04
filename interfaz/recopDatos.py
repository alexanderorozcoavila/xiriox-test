#!/usr/bin/env python
import os
import time
import psutil
import configparser
import json
from aiohttp import web
import os



direc_principal = '/home/xirioxinf/Documentos'
configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion_version = configparser.ConfigParser()
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
configuracion_version.read('/home/xirioxinf/Documentos/descarte_xiriox/config/version.cfg')
dir_encrypt = configuracion['Directorios']['dir_encrypt'] # lee el directorio de videos
#cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema
version = "v"+configuracion_version['Version']['version']
##############################################
id_dri = configuracion['ID']['id_dri']
id_embarcacion = configuracion['ID']['id_embarcacion']
cantidad_camaras = configuracion['Videos']['cantidad_camaras']
##############################################
print("-- INICIANDO SISTEMA --")

def guardarFpsBitrate(fps, bitrate, resolucion, num):
    """archivo = open(direc_principal+'/descarte_xiriox/metadatos/info/info_cam'+num,'w')
    archivo.write(fps+"fps - "+bitrate+" - "+resolucion)
    archivo.close()"""
    pass

def getBitrate(nombreCamara):
    try:
        bitrate_file = open(direc_principal+'/descarte_xiriox/grabar/output/output'+str(nombreCamara)+'.csv', 'r')
        bitrate = bitrate_file.readlines()[-1]
        bitrate_file.close()
        bitrate = bitrate.split(" ")
        while "" in bitrate:
            bitrate.remove("")
        for i in range(0,len(bitrate)):
            #print(bitrate[8])
            if "kbits/s" in bitrate[i]:
                #print("DENTRO")
                bitrate_cam = bitrate[i]
                #print(bitrate_cam)
                if "bitrate=" in bitrate_cam:
                    bitrate_cam = bitrate_cam.replace("bitrate=","")
                    return bitrate_cam
                else:
                    return bitrate_cam
                #break
            #else:
            #bitrate_cam = "--kbits/s"
            #return bitrate_cam

    except Exception as e:
        bitrate_cam = "--kbits/s"
        return bitrate_cam

def getFps(nombreCamara):
    try:
        fps_file = open(direc_principal+'/descarte_xiriox/grabar/output/output'+str(nombreCamara)+'.csv', 'r')
        fps = fps_file.readlines()[-1]
        fps_file.close()
        fps = fps.split(" ")
        while "" in fps:
            fps.remove("")
        for i in range(0,len(fps)):
            #print(fps)
            if "fps" in fps[i]:
                #print("DENTRO")
                fps_cam = fps[i+1]
                #print(fps_cam)
                return(fps_cam)
                """if "bitrate=" in fps_cam:
                    fps_cam = fps_cam.replace("bitrate=","")
                    print("bitrate_cam")
                    return fps_cam
                else:
                    return fps_cam"""
                #break
            #else:
            #bitrate_cam = "--kbits/s"
            #return bitrate_cam
    except Exception as e:
        fps_cam = "--kbits/s"
        return fps_cam

#define endpoints
def index(var2 = 1):
#def recopDatos(var2 = 1):
    #while True:
        count = 0
        fps = 0
        gps = ['0','0','0','00°00'+"'00"+'0"','00°00'+"'00"+'0"','0','0']
        gps_aux = gps
        #while True: # ciclo para ir recibiendo los frames
        seg =  time.strftime('%S') # se obtiene el segundo actual
        bitrate_cam = {}

        for cam in range(0,int(cantidad_camaras)):
           numero_cam = cam+1
           bitrate_cam['cam'+str(numero_cam)] = {'nombre':'CAM '+str(numero_cam), 'fps':getFps(int(numero_cam)), 'bitrate':getBitrate(int(numero_cam))}
        bitrate_cam1 = getBitrate(1)
        bitrate_cam2 = getBitrate(2)
        fps_cam1 = getFps(1)
        fps_cam2 = getFps(2)

        count = count+1 # cuenta un fps
        if time.strftime('%S') != seg:
            guardarFpsBitrate(str(fps), str(bitrate_cam1), str(1280)+'x'+str(720), str(var2+1))
            count = 0
        else:
            guardarFpsBitrate(str(fps), str(bitrate_cam1), str(1280)+'x'+str(720), str(var2+1))
        #print(bitrate_cam1, bitrate_cam2, fps_cam1, fps_cam2)
        fecha = time.strftime('%d-%m-%Y')
        fecha2 = time.strftime('%Y-%m-%d')
        hora =  time.strftime('%H:%M:%S')
        try:
            direct = dir_encrypt+"/"+fecha2+'/metadata/metada_temp.csv'
            f = open(direct,"r")
            gps = f.read()
            f.close()
            gps = gps.split(",     ")
            if len(gps) == 1:
                gps = gps_aux
            else:
                gps_aux = gps
        except Exception as e:
            gps = gps_aux
            print(e)
        ###########################################################################
        flag_grabacion = open(direc_principal+"/descarte_xiriox/grabar/grabar", "r")
        fg = flag_grabacion.read()
        flag_grabacion.close()
        if fg == '1': #"GRABANDO"
            estado_grabacion = 'grabando'
        else:
            if fg == '2': #"APAGANDO"
                estado_grabacion = 'apagando'
            else: #"DETENIDO"
                estado_grabacion = 'detenido'
        ###########################################################################
        configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
        try:
            disco_duro = psutil.disk_usage('/home/xirioxinf/Ext1')#cambiar directorio para detección de disco
            espacioDisponible = disco_duro[1] #Mostrar espacio libre en GB
        except Exception as e:
            disco_duro = [0]
            espacioDisponible = 0
            print(e)
        try:
            disco_duro2 = psutil.disk_usage('/home/xirioxinf/Ext2')#cambiar directorio para detección de disco
            espacioDisponible2 = disco_duro2[1] #Mostrar espacio libre en GB
        except Exception as e:
            disco_duro2 = [0]
            espacioDisponible2 = 0
            print(e)
        try:
            espacioTotal = disco_duro[0]+disco_duro2[0]
            espacioOcupado = espacioDisponible+espacioDisponible2
        except Exception as e:
            raise e
        try:
            arrayAlarmas = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/nombresAlarmas.txt', 'r+')
            dataa = arrayAlarmas.read()
            arrayAlarmas.close()
        except Exception as e:
            dataa = ''
        try:
            porcentaje = str(round((espacioOcupado*100)/espacioTotal,2))
        except Exception as e:
            porcentaje = "ERROR Disco duro externo"
        ######## PREGUNTA SI HAY ALARMA
        if dataa == "":
            #ImageDraw.Draw(img).text((60,510), "OK", fill='white', font=ttf)
            estado_alarma = 'false'
        else:
            #ImageDraw.Draw(img).text((60,510), "ALARMA", fill='white', font=ttf)
            estado_alarma = 'true'
        salida_json = {
                            'id':{
                                    'id_dri':id_dri,
                                    'id_embarcacion':id_embarcacion,
                            },
                            'camaras':bitrate_cam,
                            'gps':{
                                    'fecha':fecha,
                                    'hora':hora,
                                    'latitud':gps[3],
                                    'longitud':gps[4],
                                    'rumbo':gps[6],
                                    'velocidad':gps[5]
                            },
                            'estado_grabacion': estado_grabacion,
                            'discos_duros':{
                                    'espacio_ocupado':espacioOcupado,
                                    'espacio_total':espacioTotal,
                                    'porcentaje':porcentaje,
                            },
                            'estado_alarma': estado_alarma
        }
        return json.dumps(salida_json)
        #time.sleep(1)
