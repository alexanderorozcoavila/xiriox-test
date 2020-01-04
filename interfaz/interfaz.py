import vlc
import sys

if sys.version_info[0] < 3:
    import tkinter as tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename

# import standard libraries
import os
import pathlib
from threading import Timer,Thread,Event
import time
import platform
from PIL import Image, ImageTk
import threading
import configparser
import requests
import json
from datetime import datetime
import subprocess
# sys.path.insert(0, '/home/xirioxinf/Documentos/descarte_xiriox/scripts')
import recopDatos


class Player(tk.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, parent, title=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        if title == None:
            title = "XIORIOX - DRI"
        self.parent.title(title)
        self.bandera1 = 0
        self.bandera2 = 0
        self.bandera3 = 0
        self.bandera4 = 0
        self.bandera5 = 0
        self.bandera6 = 0
        self.bandera7 = 0
        self.bandera8 = 0

        self.api_servicio = "http://10.1.1.21:12345"
        self.rango_ip_camaras = '10.1.1.'
        self.direcFolder = '/home/xirioxinf/Documentos/descarte_xiriox/'
        self.direc_principal = '/home/xirioxinf/Documentos'
        self.ruta_archivo = self.direcFolder + "config/config.cfg"
        self.ruta_archivo_version = self.direcFolder +"config/version.cfg"
        self.credenciales_camaras = "admin:xiriox3000"
        self.credencial_root_sistema = "xiriox3000"

        self.logosistema = self.direcFolder + "img/logodri.png"

        self.puerto_camaras_stream = ':554'
        self.protocolo_cam_stream = 'rtsp'
        self.reinicio_automatico = False

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        sec_izq = 300
        sec_der = sw - 300
        sh_camaras = sh - 300
        configuracion = configparser.ConfigParser()
        configuracion.read(self.ruta_archivo)
        version_sistema = configparser.ConfigParser()
        version_sistema.read(self.ruta_archivo_version)


        # self.frame_sec_der=tk.Frame(self.parent, width=sw, height=sh_camaras, background="#602066")
        # self.frame_sec_der.grid(sticky="S",row=0, column=1)
        # #Medidas seccion derecha
        sec_der_top = sh - 300
        sec_der_bottom = 300
        self.frame_sec_der_top=tk.Frame(self.parent, width=sw, height=sh_camaras, background="#602066")
        self.frame_sec_der_top.grid(row=0, column=0)

        self.load = Image.open(self.logosistema)
        basewidth = 300
        wpercent = (basewidth/float(self.load.size[0]))
        hsize = int((float(self.load.size[1])*float(wpercent)))
        self.load = self.load.resize((basewidth,hsize), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(self.load)

        cam_w = sw / 3
        cam_h_temp = sh_camaras / 2
        cam_titulo_h = 5
        cam_h = cam_h_temp - 20

        self.frame_sec_bottom=tk.Frame(self.parent, width=sw, height=260, background="#602066")
        self.frame_sec_bottom.grid(row=1, column=0)

        self.frame_sec_bottom_1=tk.Frame(self.frame_sec_bottom, width=cam_w, height=260, background="#602066")
        self.frame_sec_bottom_1.grid(sticky="W",row=0, column=0)

        #####Titulos
        self.linea_titulo_general=tk.Frame(self.frame_sec_bottom_1, width=cam_w, height=20, background="#602066")
        self.linea_titulo_general.grid(sticky="W",row=0, column=0)

        self.frame_sec_izq_title_4 = tk.Label(self.linea_titulo_general, text='Datos Generales')
        self.frame_sec_izq_title_4.grid(row=0, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        self.frame_sec_bottom2_linea_4=tk.Frame(self.linea_titulo_general, width=cam_w-40, height=1, background="#fff")
        self.frame_sec_bottom2_linea_4.grid(row=1, column=0)

        #####linea 1####
        self.frame_sec_bottom_linea_2=tk.Frame(self.frame_sec_bottom_1, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_2.grid(sticky="W",row=2, column=0)

        self.frame_sec_izq_title_1 = tk.Label(self.frame_sec_bottom_linea_2, text='   Fecha:')
        self.frame_sec_izq_title_1.grid(row=2, column=0)
        self.frame_sec_izq_title_1.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.date_time_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_1 = tk.Label(self.frame_sec_bottom_linea_2, textvariable=self.date_time_text)
        self.frame_sec_izq_title_1.grid(row=2, column=1)
        self.frame_sec_izq_title_1.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 2 ####
        self.frame_sec_bottom_linea_3=tk.Frame(self.frame_sec_bottom_1, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_3.grid(sticky="W",row=3, column=0)

        self.frame_sec_izq_title_2 = tk.Label(self.frame_sec_bottom_linea_3, text='   DRI ID:')
        self.frame_sec_izq_title_2.grid(sticky="W",row=3, column=0)
        self.frame_sec_izq_title_2.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.id_dri_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_2 = tk.Label(self.frame_sec_bottom_linea_3, textvariable=self.id_dri_text)
        self.frame_sec_izq_title_2.grid(sticky="W",row=3, column=1)
        self.frame_sec_izq_title_2.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 3 ####
        self.frame_sec_bottom_linea_4=tk.Frame(self.frame_sec_bottom_1, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_4.grid(sticky="W",row=4, column=0)

        self.frame_sec_izq_title_3 = tk.Label(self.frame_sec_bottom_linea_4, text='   EMBARCACION ID:')
        self.frame_sec_izq_title_3.grid(sticky="W",row=4, column=0)
        self.frame_sec_izq_title_3.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.id_embarcacion_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_3 = tk.Label(self.frame_sec_bottom_linea_4, textvariable=self.id_embarcacion_text)
        self.frame_sec_izq_title_3.grid(sticky="W",row=4, column=1)
        self.frame_sec_izq_title_3.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 4 ####
        self.frame_sec_bottom_linea_5=tk.Frame(self.frame_sec_bottom_1, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_5.grid(sticky="W",row=5, column=0)

        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_5, text='   LATITUD:')
        self.frame_sec_izq_title_4.grid(sticky="W",row=5, column=0)
        self.frame_sec_izq_title_4.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.latitud_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_5, textvariable=self.latitud_text)
        self.frame_sec_izq_title_4.grid(sticky="W",row=5, column=1)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 5 ####
        self.frame_sec_bottom_linea_6=tk.Frame(self.frame_sec_bottom_1, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_6.grid(sticky="W",row=6, column=0)

        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_5, text='   LONGITUD:')
        self.frame_sec_izq_title_4.grid(sticky="W",row=6, column=0)
        self.frame_sec_izq_title_4.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.longitud_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_5, textvariable=self.longitud_text)
        self.frame_sec_izq_title_4.grid(sticky="W",row=6, column=1)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 6 ####
        self.frame_sec_bottom_linea_7=tk.Frame(self.frame_sec_bottom_1, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_7.grid(sticky="W",row=7, column=0)

        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_7, text='   RUMBO:')
        self.frame_sec_izq_title_4.grid(sticky="W",row=7, column=0)
        self.frame_sec_izq_title_4.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.rumbo_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_7, textvariable=self.rumbo_text)
        self.frame_sec_izq_title_4.grid(sticky="W",row=7, column=1)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 7 ####
        self.frame_sec_bottom_linea_8=tk.Frame(self.frame_sec_bottom_1, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_8.grid(sticky="W",row=8, column=0)

        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_6, text='   VELOCIDAD:')
        self.frame_sec_izq_title_4.grid(sticky="W",row=8, column=0)
        self.frame_sec_izq_title_4.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.velocidad_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_6, textvariable=self.velocidad_text)
        self.frame_sec_izq_title_4.grid(sticky="W",row=8, column=1)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ################################################# panel discos

        self.frame_sec_bottom_2=tk.Frame(self.frame_sec_bottom, width=cam_w, height=260, background="#602066")
        self.frame_sec_bottom_2.grid(sticky="W",row=0, column=1)

        #####Titulos
        self.linea_titulo_general=tk.Frame(self.frame_sec_bottom_2, width=cam_w, height=20, background="#602066")
        self.linea_titulo_general.grid(sticky="W",row=0, column=0)

        self.frame_sec_izq_title_4 = tk.Label(self.linea_titulo_general, text='Disco Duros')
        self.frame_sec_izq_title_4.grid(row=0, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        self.frame_sec_bottom2_linea_4=tk.Frame(self.linea_titulo_general, width=cam_w-40, height=1, background="#fff")
        self.frame_sec_bottom2_linea_4.grid(row=1, column=0)

        #####linea 1####
        self.frame_sec_bottom_linea_2=tk.Frame(self.frame_sec_bottom_2, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_2.grid(sticky="W",row=2, column=0)

        self.frame_sec_izq_title_1 = tk.Label(self.frame_sec_bottom_linea_2, text='Disco usado (%):')
        self.frame_sec_izq_title_1.grid(row=2, column=0)
        self.frame_sec_izq_title_1.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.porcentaje_disco_usado = tk.IntVar(value = '---- no data ----')
        self.frame_sec_izq_title_1 = tk.Label(self.frame_sec_bottom_linea_2, textvariable=self.porcentaje_disco_usado)
        self.frame_sec_izq_title_1.grid(row=2, column=1)
        self.frame_sec_izq_title_1.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 2 ####
        self.frame_sec_bottom_linea_3=tk.Frame(self.frame_sec_bottom_2, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_3.grid(sticky="W",row=3, column=0)

        self.frame_sec_izq_title_2 = tk.Label(self.frame_sec_bottom_linea_3, text='Disco disponible (%):')
        self.frame_sec_izq_title_2.grid(sticky="W",row=3, column=0)
        self.frame_sec_izq_title_2.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.porcentaje_disco_disponible = tk.IntVar(value = '---- no data ----')
        self.frame_sec_izq_title_2 = tk.Label(self.frame_sec_bottom_linea_3, textvariable=self.porcentaje_disco_disponible)
        self.frame_sec_izq_title_2.grid(sticky="W",row=3, column=1)
        self.frame_sec_izq_title_2.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 3 ####
        self.frame_sec_bottom_linea_4=tk.Frame(self.frame_sec_bottom_2, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_4.grid(sticky="W",row=4, column=0)

        self.frame_sec_izq_title_3 = tk.Label(self.frame_sec_bottom_linea_4, text='Total disco:')
        self.frame_sec_izq_title_3.grid(sticky="W",row=4, column=0)
        self.frame_sec_izq_title_3.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.total_disco = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_3 = tk.Label(self.frame_sec_bottom_linea_4, textvariable=self.total_disco)
        self.frame_sec_izq_title_3.grid(sticky="W",row=4, column=1)
        self.frame_sec_izq_title_3.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 4 ####
        self.frame_sec_bottom_linea_5=tk.Frame(self.frame_sec_bottom_2, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_5.grid(sticky="W",row=5, column=0)

        # self.latitud_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_5, text='')
        self.frame_sec_izq_title_4.grid(sticky="W",row=5, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 5 ####
        self.frame_sec_bottom_linea_6=tk.Frame(self.frame_sec_bottom_2, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_6.grid(sticky="W",row=6, column=0)

        # self.longitud_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_5, text='')
        self.frame_sec_izq_title_4.grid(sticky="W",row=6, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 6 ####
        self.frame_sec_bottom_linea_7=tk.Frame(self.frame_sec_bottom_2, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_7.grid(sticky="W",row=7, column=0)

        # self.rumbo_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_7, text='')
        self.frame_sec_izq_title_4.grid(sticky="W",row=7, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 7 ####
        self.frame_sec_bottom_linea_8=tk.Frame(self.frame_sec_bottom_2, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_8.grid(sticky="W",row=8, column=0)

        # self.velocidad_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_6, text='')
        self.frame_sec_izq_title_4.grid(sticky="W",row=8, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ############# panel status sistemas

        self.frame_sec_bottom_3=tk.Frame(self.frame_sec_bottom, width=cam_w, height=260, background="#602066")
        self.frame_sec_bottom_3.grid(sticky="W",row=0, column=2)

        #####Titulos
        self.linea_titulo_general=tk.Frame(self.frame_sec_bottom_3, width=cam_w, height=20, background="#602066")
        self.linea_titulo_general.grid(sticky="W",row=0, column=0)

        self.frame_sec_izq_title_4 = tk.Label(self.linea_titulo_general, text='Estados del Sistema')
        self.frame_sec_izq_title_4.grid(row=0, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        self.frame_sec_bottom2_linea_4=tk.Frame(self.linea_titulo_general, width=cam_w-40, height=1, background="#fff")
        self.frame_sec_bottom2_linea_4.grid(row=1, column=0)

        #####linea 1####
        self.frame_sec_bottom_linea_2=tk.Frame(self.frame_sec_bottom_3, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_2.grid(sticky="W",row=2, column=0)

        self.frame_sec_izq_title_1 = tk.Label(self.frame_sec_bottom_linea_2, text='Conectividad:')
        self.frame_sec_izq_title_1.grid(row=2, column=0)
        self.frame_sec_izq_title_1.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.conectividad = tk.IntVar(value = '---- no data ----')
        self.frame_sec_izq_title_con = tk.Label(self.frame_sec_bottom_linea_2, textvariable=self.conectividad)
        self.frame_sec_izq_title_con.grid(row=2, column=1)
        self.frame_sec_izq_title_con.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 2 ####
        self.frame_sec_bottom_linea_3=tk.Frame(self.frame_sec_bottom_3, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_3.grid(sticky="W",row=3, column=0)

        self.frame_sec_izq_title_2 = tk.Label(self.frame_sec_bottom_linea_3, text='Estado:')
        self.frame_sec_izq_title_2.grid(sticky="W",row=3, column=0)
        self.frame_sec_izq_title_2.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.estado_sistema = tk.IntVar(value = '---- no data ----')
        self.frame_sec_izq_title_2 = tk.Label(self.frame_sec_bottom_linea_3, textvariable=self.estado_sistema)
        self.frame_sec_izq_title_2.grid(sticky="W",row=3, column=1)
        self.frame_sec_izq_title_2.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 3 ####
        self.frame_sec_bottom_linea_4=tk.Frame(self.frame_sec_bottom_3, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_4.grid(sticky="W",row=4, column=0)

        self.frame_sec_izq_title_3 = tk.Label(self.frame_sec_bottom_linea_4, text='Grabación:')
        self.frame_sec_izq_title_3.grid(sticky="W",row=4, column=0)
        self.frame_sec_izq_title_3.config(fg="#3edeab",bg="#602066",font=("Verdana",15))

        self.grabacion = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_3 = tk.Label(self.frame_sec_bottom_linea_4, textvariable=self.grabacion)
        self.frame_sec_izq_title_3.grid(sticky="W",row=4, column=1)
        self.frame_sec_izq_title_3.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 4 ####
        self.frame_sec_bottom_linea_5=tk.Frame(self.frame_sec_bottom_3, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_5.grid(sticky="W",row=5, column=0)

        # self.latitud_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_5, text='')
        self.frame_sec_izq_title_4.grid(sticky="W",row=5, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 5 ####
        self.frame_sec_bottom_linea_6=tk.Frame(self.frame_sec_bottom_3, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_6.grid(sticky="W",row=6, column=0)

        # self.longitud_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_5, text='')
        self.frame_sec_izq_title_4.grid(sticky="W",row=6, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 6 ####
        self.frame_sec_bottom_linea_7=tk.Frame(self.frame_sec_bottom_3, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_7.grid(sticky="W",row=7, column=0)

        # self.rumbo_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_7, text='')
        self.frame_sec_izq_title_4.grid(sticky="W",row=7, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))

        ###### linea 7 ####
        self.frame_sec_bottom_linea_8=tk.Frame(self.frame_sec_bottom_3, width=cam_w, height=20, background="#602066")
        self.frame_sec_bottom_linea_8.grid(sticky="W",row=8, column=0)

        # self.velocidad_text = tk.IntVar(value = '--- No data ---')
        self.frame_sec_izq_title_4 = tk.Label(self.frame_sec_bottom_linea_6, text='')
        self.frame_sec_izq_title_4.grid(sticky="W",row=8, column=0)
        self.frame_sec_izq_title_4.config(fg="white",bg="#602066",font=("Verdana",15))


        ############# panel logo

        self.frame_sec_logo=tk.Frame(self.parent, width=sw, height=40, background="#602066")
        self.frame_sec_logo.grid(sticky="E",row=2, column=0)

        self.imageLogo = tk.Label(self.frame_sec_logo,image=self.render)
        self.imageLogo.grid(row=0, column=0)
        self.imageLogo.config(fg="white",bg="#602066")




        # Medidas laterales
        # self.frame_sec_izq=tk.Frame(self.parent, width=sec_izq, height=sh_t, background="#602066")
        # self.frame_sec_izq.grid(row=0, column=0)
        # self.frame_sec_izq_title=tk.Frame(self.frame_sec_izq, width=sec_izq, height=200, background="#602066")
        # self.frame_sec_izq_title.grid(sticky="W",row=0, column=0)
        # self.date_time_text = tk.IntVar(value = 'No date')
        # self.frame_sec_izq_title_1 = tk.Label(self.frame_sec_bottom_1, textvariable=self.date_time_text)
        # self.frame_sec_izq_title_1.grid(sticky="W",row=0, column=0)
        # self.frame_sec_izq_title_1.config(fg="white",bg="#602066",font=("Verdana",15))
        #

        #

        #
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="")
        # self.frame_sec_izq_content_linea.grid(row=7, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="")
        # self.frame_sec_izq_content_linea.grid(row=8, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.estado_alarma = tk.IntVar(value = '--- No data ---')
        self.style_btn_alarma = False
        # self.frame_sec_izq_content_1 = tk.Button(self.frame_sec_izq_title, textvariable=self.estado_alarma)
        # self.frame_sec_izq_content_1.grid(row=9, column=0)
        # self.frame_sec_izq_content_1.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="")
        # self.frame_sec_izq_content_linea.grid(row=10, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="")
        # self.frame_sec_izq_content_linea.grid(row=11, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="DISCO DURO")
        # self.frame_sec_izq_content_linea.grid(row=12, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.frame_sec_izq_content_linea1= tk.Frame(self.frame_sec_izq_title,width=sec_izq, height=2, background="#602066")
        # self.frame_sec_izq_content_linea1.grid(row=13, column=0)
        # self.frame_sec_izq_content_linea2 = tk.Frame(self.frame_sec_izq_content_linea1,width=10, height=1, background="#602066")
        # self.frame_sec_izq_content_linea2.grid(row=0, column=0)
        # self.frame_sec_izq_content_linea3 = tk.Frame(self.frame_sec_izq_content_linea1,width=sec_izq-20, height=1, background="#fff")
        # self.frame_sec_izq_content_linea3.grid(row=0, column=1)
        # self.frame_sec_izq_content_linea4 = tk.Frame(self.frame_sec_izq_content_linea1,width=10, height=1, background="#602066")
        # self.frame_sec_izq_content_linea4.grid(row=0, column=2)
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="")
        # self.frame_sec_izq_content_linea.grid(row=14, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.frame_sec_izq_content_bar1= tk.Frame(self.frame_sec_izq_title,width=sec_izq, height=20, background="#602066")
        # self.frame_sec_izq_content_bar1.grid(row=16, column=0)
        # self.frame_sec_izq_content_bar2 = tk.Frame(self.frame_sec_izq_content_bar1,width=10, height=35, background="#602066")
        # self.frame_sec_izq_content_bar2.grid(row=0, column=0)
        # self.por_disc_100 = sec_izq - 20
        # self.por_disc_x = 100
        # self.w_por_disc_ = (self.por_disc_x * self.por_disc_100) / 100
        # self.w_por_disc_rest =  self.por_disc_100 - self.w_por_disc_
        # self.frame_sec_izq_content_bar3 = tk.Frame(self.frame_sec_izq_content_bar1,width=self.w_por_disc_-10, height=35, background="#d4d2d4")
        # self.frame_sec_izq_content_bar3.grid(row=0, column=1)
        # self.frame_sec_izq_content_bar4 = tk.Frame(self.frame_sec_izq_content_bar1,width=self.w_por_disc_rest-10, height=35, background="#8f3886")
        # self.frame_sec_izq_content_bar4.grid(row=0, column=2)
        # self.frame_sec_izq_content_bar5 = tk.Frame(self.frame_sec_izq_content_bar1,width=10, height=35, background="#602066")
        # self.frame_sec_izq_content_bar5.grid(row=0, column=3)
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="")
        # self.frame_sec_izq_content_linea.grid(row=17, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.estado_disco = tk.IntVar(value = '--- No data ---')
        # self.style_btn_disco = False
        # self.frame_sec_izq_content_boton1 = tk.Button(self.frame_sec_izq_title, textvariable=self.estado_disco)
        # self.frame_sec_izq_content_boton1.grid(row=18, column=0)
        # self.frame_sec_izq_content_boton1.config(bg="#602066",fg="#8f3886",font=("Verdana",15))
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="")
        # self.frame_sec_izq_content_linea.grid(row=19, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # self.frame_sec_izq_content_linea = tk.Label(self.frame_sec_izq_title, text="")
        # self.frame_sec_izq_content_linea.grid(row=20, column=0)
        # self.frame_sec_izq_content_linea.config(fg="white",bg="#602066",font=("Verdana",15))
        # sh_content = 150
        # self.frame_sec_izq_content=tk.Frame(self.frame_sec_izq, width=sec_izq, height=sh_content, background="#602066")
        # self.frame_sec_izq_content.grid(row=1, column=0)
        # self.frame_sec_izq_content_foo_1=tk.Frame(self.frame_sec_izq_content, width=sec_izq, height=130, background="#602066")
        # self.frame_sec_izq_content_foo_1.grid(row=0, column=0)
        # self.frame_sec_izq_content_foo_1=tk.Frame(self.frame_sec_izq_content, width=sec_izq, height=20, background="#602066")
        # self.frame_sec_izq_content_foo_1.grid(row=1, column=0)
        # self.frame_sec_izq_content_foo_1_text = tk.Label(self.frame_sec_izq_content_foo_1, text=str(version_sistema['Version']['version']) + "      www.xiriox.com")
        # self.frame_sec_izq_content_foo_1_text.grid(row=20, column=0)
        # self.frame_sec_izq_content_foo_1_text.config(fg="white",bg="#602066",font=("Verdana",12))

        # self.frame_sec_der_bootom=tk.Frame(self.frame_sec_der, width=sec_der, height=sec_der_bottom, background="#602066")
        # self.frame_sec_der_bootom.grid(row=1, column=0)

        # #Session Camaras

        #
        # self.bootom_1 = tk.Frame(self.frame_sec_der_bootom, width=cam_w, height=300, background="#602066")
        # self.bootom_1.grid(row=0, column=0)
        # self.bootom_2 = tk.Frame(self.frame_sec_der_bootom, width=cam_w, height=300, background="#602066")
        # self.bootom_2.grid(row=0, column=1)
        # self.bootom_3 = tk.Frame(self.frame_sec_der_bootom, width=cam_w, height=300, background="#602066")
        # self.bootom_3.grid(row=0, column=2)
        #
        # self.imageLogo = tk.Label(self.bootom_3,image=self.render)
        # self.imageLogo.grid(row=0, column=0)
        # self.imageLogo.config(fg="white",bg="#602066")

        self.play_obj = {}
        self.play_obj['player1'] = None
        self.play_obj['player1_status'] = False
        self.play_obj['bandera1'] = 0
        self.play_obj['bitrate_text_1'] = tk.IntVar(value = '--- No data ---')

        # self.videopanel1_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        # self.videopanel1_titulo.grid(row=0, column=0)



        self.play_obj['videopanel1'] = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.play_obj['videopanel1'].grid(row=0, column=0)

        self.labelBitrate1 = tk.Label(self.frame_sec_der_top, textvariable=self.play_obj['bitrate_text_1'])
        self.labelBitrate1.grid(sticky="NW",row=0, column=0)
        self.labelBitrate1.config(fg="white",bg="#602066",font=("Verdana",10))


        self.play_obj['player2'] = None
        self.play_obj['player2_status'] = False
        self.play_obj['bandera2'] = 0
        self.play_obj['bitrate_text_2'] = tk.IntVar(value = '--- No data ---')

        # self.videopanel2_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        # self.videopanel2_titulo.grid(row=0, column=1)

        self.play_obj['videopanel2'] = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.play_obj['videopanel2'].grid(row=0, column=1)
        self.labelBitrate2 = tk.Label(self.frame_sec_der_top, textvariable=self.play_obj['bitrate_text_2'])
        self.labelBitrate2.grid(sticky="NW",row=0, column=1)
        self.labelBitrate2.config(fg="white",bg="#602066",font=("Verdana",10))

        self.play_obj['player3'] = None
        self.play_obj['player3_status'] = False
        self.play_obj['bandera3'] = 0
        # self.videopanel3_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        # self.videopanel3_titulo.grid(row=0, column=2)
        self.play_obj['bitrate_text_3'] = tk.IntVar(value = '--- No data ---')

        self.play_obj['videopanel3'] = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.play_obj['videopanel3'].grid(row=0, column=2)
        self.labelBitrate3 = tk.Label(self.frame_sec_der_top, textvariable=self.play_obj['bitrate_text_3'])
        self.labelBitrate3.grid(sticky="NW",row=0, column=2)
        self.labelBitrate3.config(fg="white",bg="#602066",font=("Verdana",10))

        self.play_obj['player4'] = None
        self.play_obj['player4_status'] = False
        self.play_obj['bandera4'] = 0
        # self.videopanel4_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        # self.videopanel4_titulo.grid(row=2, column=0)
        self.play_obj['bitrate_text_4'] = tk.IntVar(value = '--- No data ---')

        self.play_obj['videopanel4'] = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.play_obj['videopanel4'].grid(row=1, column=0)
        self.labelBitrate4 = tk.Label(self.frame_sec_der_top, textvariable=self.play_obj['bitrate_text_4'])
        self.labelBitrate4.grid(sticky="NW",row=1, column=0)
        self.labelBitrate4.config(fg="white",bg="#602066",font=("Verdana",10))

        self.play_obj['player5'] = None
        self.play_obj['player5_status'] = False
        self.play_obj['bandera5'] = 0
        # self.videopanel5_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        # self.videopanel5_titulo.grid(row=2, column=1)
        self.play_obj['bitrate_text_5'] = tk.IntVar(value = '--- No data ---')

        self.play_obj['videopanel5'] = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.play_obj['videopanel5'].grid(row=1, column=1)
        self.labelBitrate5 = tk.Label(self.frame_sec_der_top, textvariable=self.play_obj['bitrate_text_5'])
        self.labelBitrate5.grid(sticky="NW",row=1, column=1)
        self.labelBitrate5.config(fg="white",bg="#602066",font=("Verdana",10))

        self.play_obj['player6'] = None
        self.play_obj['player6_status'] = False
        self.play_obj['bandera6'] = 0
        # self.videopanel6_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        # self.videopanel6_titulo.grid(row=2, column=2)
        self.play_obj['bitrate_text_6'] = tk.IntVar(value = 'No disponible')

        self.play_obj['videopanel6'] = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.play_obj['videopanel6'].grid(row=1, column=2)
        self.labelBitrate6 = tk.Label(self.frame_sec_der_top, textvariable=self.play_obj['bitrate_text_6'])
        self.labelBitrate6.grid(sticky="NW",row=1, column=2)
        self.labelBitrate6.config(fg="white",bg="#602066",font=("Verdana",10))

        self.Instance = vlc.Instance()
        self.cantidad_camaras = configuracion['Videos']['cantidad_camaras']
        self.cam = {}
        self.t = {}
        self.cam_conectadas = configparser.ConfigParser()
        temp_cam = {}
        for i in range(0,int(self.cantidad_camaras)):
            temp_cam.update({'CAM'+str(i+1) :'true'} )
            url = self.protocolo_cam_stream+'://'+self.credenciales_camaras+'@'+self.rango_ip_camaras+configuracion['IP']['cam'+str(i+1)]+self.puerto_camaras_stream
            self.cam[str(i+1)] = self.rango_ip_camaras+configuracion['IP']['cam'+str(i+1)]
            self.play1(url,str(i+1))
            self.t[str(i+1)] = threading.Thread(target=self.set_bitrate1,args=(str(i+1),))
            self.t[str(i+1)].start()

        self.cam_conectadas['CAM'] = temp_cam
        with open(self.direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
            self.cam_conectadas.write(configfile)

        self.t['estados'] = threading.Thread(target=self.estado)
        self.t['estados'].start()

    def play1(self,url,id):
        self.play_obj['player'+str(id)] = self.Instance.media_player_new()
        Media = self.Instance.media_new(url)
        self.play_obj['player'+str(id)].set_media(Media)
        self.play_obj['player'+str(id)].set_xwindow(self.play_obj['videopanel'+str(id)].winfo_id())
        if self.play_obj['player'+str(id)].play() == -1:
            self.errorDialog("error en conexion...")

    def stop(self,player):
        player.stop()
        # reset the time slider
        self.timeslider.set(0)

    def restart(self,player):
        if player.play() == -1:
            self.errorDialog("error en conexion...")

    def check_ping(self,ip):
        response = os.system("ping -c 1 -W 1 " + ip)
        if response == 0:
            pingstatus = True
        else:
            pingstatus = False
        return pingstatus

    def set_bitrate1(self,id):
        configuracion = configparser.ConfigParser() # abre archivo de configuración
        configuracion.read(self.ruta_archivo) # lee el archivo de configuración
        ip = self.rango_ip_camaras+configuracion['IP']['cam'+str(id)]
        url = self.protocolo_cam_stream+'://'+self.credenciales_camaras+'@'+self.rango_ip_camaras+configuracion['IP']['cam'+str(id)]+self.puerto_camaras_stream
        if str(self.play_obj['player'+str(id)].get_state()) == 'State.Ended':
            self.play_obj['bitrate_text_'+str(id)].set('conectando...')
            self.conectividad.set(' itermitente ')
            self.frame_sec_izq_title_con.config(fg="black",bg="yellow",font=("Verdana",10))
            self.play_obj['player'+str(id)].stop()
            self.play_obj['player'+str(id)].play()
            self.play_obj['bandera'+str(id)] = self.play_obj['bandera'+str(id)] + 1
            self.cam_conectadas['CAM']['cam'+str(id)] = 'false'
            with open(self.direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
                self.cam_conectadas.write(configfile)
        else:
            if self.check_ping(ip):
                response = True
                if response:
                    r1 = recopDatos.index()
                    r = json.loads(r1)
                    nombre_camara = ""
                    try:
                        nombre_camara = r['camaras']['cam'+str(id)]['nombre']
                        if str(nombre_camara) == "None":
                            nombre_camara = "--"
                    except:
                        nombre_camara = "--"
                    fps_camara = ""
                    try:
                        fps_camara = r['camaras']['cam'+str(id)]['fps']
                        if str(fps_camara) == "None":
                            fps_camara = "--"
                    except:
                        fps_camara = "--"
                    bitrate_camara = ""
                    try:
                        bitrate_camara = r['camaras']['cam'+str(id)]['bitrate']
                        if str(bitrate_camara) == "None":
                            bitrate_camara = "--"
                    except:
                        bitrate_camara = "--"
                    texto = str(nombre_camara) + " " + str(ip) + " " + " - FPS: " + str(fps_camara) + " bitrate: " + str(bitrate_camara)
                    self.play_obj['bitrate_text_'+str(id)].set(texto)
                    self.play_obj['bandera'+str(id)] = 0
                    self.conectividad.set(' ok ')
                    self.frame_sec_izq_title_con.config(fg="white",bg="green",font=("Verdana",10))
                    self.cam_conectadas['CAM']['cam'+str(id)] = 'true'
                    with open(self.direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
                        self.cam_conectadas.write(configfile)
                else:
                    self.play_obj['bitrate_text_'+str(id)].set('conectando...')
                    self.conectividad.set(' itermitente ')
                    self.frame_sec_izq_title_con.config(fg="black",bg="yellow",font=("Verdana",10))
                    self.play_obj['bandera'+str(id)] = self.play_obj['bandera'+str(id)] + 1
                    self.cam_conectadas['CAM']['cam'+str(id)] = 'false'
                    with open(self.direc_principal+'/descarte_xiriox/csv/cam_conectadas.ini', 'w') as configfile:
                        self.cam_conectadas.write(configfile)
            else:
                self.play_obj['bitrate_text_'+str(id)].set('conectando...')
                self.conectividad.set(' itermitente ')
                self.frame_sec_izq_title_con.config(fg="black",bg="yellow",font=("Verdana",10))
                self.play_obj['bandera'+str(id)] = self.play_obj['bandera'+str(id)] + 1
        self.labelBitrate1.after(250, self.set_bitrate1,id)

    def estado(self):
        response = True
        if response:
            r1 = recopDatos.index()
            r = json.loads(r1)
            texto =r['gps']['fecha'] + '  ' + r['gps']['hora']
            self.date_time_text.set(texto)
            texto =r['id']['id_dri']
            self.id_dri_text.set(texto)
            texto =r['id']['id_embarcacion']
            self.id_embarcacion_text.set(texto)
            texto =r['gps']['latitud']
            self.latitud_text.set(texto)
            texto =r['gps']['longitud']
            self.longitud_text.set(texto)
            texto =r['gps']['rumbo']
            self.rumbo_text.set(texto)
            texto =r['gps']['velocidad']
            self.velocidad_text.set(texto)
            texto = r['estado_alarma']
            texto_disco = r['estado_grabacion']
            if texto == "false":
                self.estado_sistema.set(" OK ")
                self.frame_sec_izq_title_2.config(fg="white",bg="green",font=("Verdana",10))
            else:
                self.estado_sistema.set(" Error ")
                self.frame_sec_izq_title_2.config(fg="white",bg="red",font=("Verdana",10))
            pd = float(r['discos_duros']['porcentaje'])
            self.por_disc_x = int(pd)
            self.porcentaje_disco_usado.set(self.por_disc_x)
            self.porcentaje_disco_disponible.set(100-self.por_disc_x)
            
            rs1 = (int(r['discos_duros']['espacio_ocupado'])/1024)/1024
            rs = round(rs1, 2) + str(" MB")
            self.total_disco.set(rs)
            if texto_disco == "grabando":
                self.grabacion.set(" Ok ")
                self.frame_sec_izq_title_3.config(fg="white",bg="green",font=("Verdana",10))
            else:
                self.grabacion.set(" Error ")
                self.frame_sec_izq_title_3.config(fg="white",bg="red",font=("Verdana",10))

        else:
            texto = "--- No data ---"
            self.date_time_text.set(texto)
            self.id_dri_text.set(texto)
            self.id_embarcacion_text.set(texto)
            self.latitud_text.set(texto)
            self.longitud_text.set(texto)
            self.rumbo_text.set(texto)
            self.velocidad_text.set(texto)
            self.estado_disco.set("--- No data ---")
            if self.play_obj['bandera1'] >= 15:
                # self.date_time_text.set("  Estado: --verificando.")
                error_camaras = False
                if self.verificarCamaras():
                    # self.id_dri_text.set("  Estado: --error camaras.")
                    error_camaras = True
                else:
                    error_camaras = False
                    # self.id_dri_text.set("  Estado: --camaras OK.")

                # self.id_embarcacion_text.set("  Estado: --verificando.")
                error_discos = False
                if self.verificandoDiscos():
                    # self.latitud_text.set("  Estado: --error discos.")
                    error_discos = True
                else:
                    error_discos = False
                    # self.latitud_text.set("  Estado: --discos OK.")
                if error_discos and error_camaras:
                    # self.longitud_text.set("  Estado: reiniciando sistema")
                    if self.reinicio_automatico:
                        os.system(self.direcFolder+"/script/log.py \"Reinicio de sistema\"")
                        os.system("echo "+self.credencial_root_sistema+" | sudo -S reboot")
        self.frame_sec_izq_title_1.after(250, self.estado)

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        print('error')
        edialog = tk.tkMessageBox.showerror(self, 'Error', errormessage)

    def verificarCamaras(self):
        cantidad_camaras = self.cantidad_camaras
        cantidad_errores = 0
        for i in range(0,int(cantidad_camaras)):
            ip = self.cam[str(i+1)]
            if self.check_ping(ip) == False:
                cantidad_errores = cantidad_errores + 1
        error_camaras = False
        if str(cantidad_errores) == str(cantidad_camaras):
            error_camaras = True
        return error_camaras

    def verificandoDiscos(self):
        configuracion = configparser.ConfigParser()
        configuracion.read(self.ruta_archivo)
        discos= self.recDiscos()
        error_discos = False
        if discos:
            error_disco_mount = 0
            cant_discos = configuracion['Externos']['cant_discos']
            for i in range(0,int(cant_discos)):
                if str(discos[i]) == str(configuracion['Externos']['ext'+str(i+1)]):
                    error_disco_mount = error_disco_mount + 1
            if error_disco_mount >= cant_discos:
                error_discos = True
        else:
            error_discos = True
        return error_discos

    def recDiscos(self):
        array = []
        try:
            test1 = subprocess.check_output("echo "+self.credencial_root_sistema+" | sudo -S sudo lsblk -fm | grep sd", shell=True)
            text_decode = test1.decode('utf-8')
            text_decode = str(text_decode).split("\n")
            for elemento in text_decode:
                elemento = elemento.split(" ")
                while " " in elemento or "" in elemento:
                    try:
                        elemento.remove(" ")
                    except:
                        pass
                    try:
                        elemento.remove("")
                    except:
                        pass
                array.append(elemento)
            var_sdx = []
            for discos in array:
                print(discos[0])
                if "T" in discos[1] and "Int1" not in discos and "Int2" not in discos and "Int3" not in discos:
                    try:
                        if len(discos[0]) == 3:
                            var_sdx.append(discos[0])
                    except:
                        print("error")
        except Exception as e:
            var_sdx = False
        return var_sdx

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"):
        Tk_get_root.root= tk.Tk()
    return Tk_get_root.root

def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()
    root.destroy()
    os._exit(1)

if __name__ == "__main__":
    root = Tk_get_root()
    root.protocol("WM_DELETE_WINDOW", _quit)
    player = Player(root, title="XIRIOX")
    root.configure(background='#602066')
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(str(sw)+'x'+str(sh))
    root.attributes("-fullscreen", True)
    root.mainloop()
