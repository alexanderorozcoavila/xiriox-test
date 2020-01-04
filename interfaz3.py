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


class Player(tk.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, parent, title=None):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        if title == None:
            title = "XIORIOX"
        self.parent.title(title)

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        sec_izq = 300
        sec_der = sw - 300
        # Medidas laterales
        self.frame_sec_izq=tk.Frame(self.parent, width=sec_izq, height=sh, background="#602066")
        self.frame_sec_izq.grid(row=0, column=0)
        self.frame_sec_der=tk.Frame(self.parent, width=sec_der, height=sh, background="#602066")
        self.frame_sec_der.grid(row=0, column=1)

        #Medidas seccion derecha
        sec_der_top = sh - 300
        sec_der_bottom = 300
        self.frame_sec_der_top=tk.Frame(self.frame_sec_der, width=sec_der, height=sec_der_top, background="#602066")
        self.frame_sec_der_top.grid(row=0, column=0)
        self.frame_sec_der_bootom=tk.Frame(self.frame_sec_der, width=sec_der, height=sec_der_bottom, background="#602066")
        self.frame_sec_der_bootom.grid(row=1, column=0)

        #Session Camaras
        cam_w = sec_der / 3
        cam_h_temp = sec_der_top / 2
        cam_titulo_h = 20
        cam_h = cam_h_temp - (cam_titulo_h * 2)

        self.player1 = None

        self.videopanel1_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        self.videopanel1_titulo.grid(row=0, column=0)
        self.bitrate_text_1 = tk.IntVar(value = 0)
        self.labelBitrate1 = tk.Label(self.videopanel1_titulo, textvariable=self.bitrate_text_1)
        self.labelBitrate1.grid(row=0, column=0)
        self.labelBitrate1.config(fg="white",bg="#602066",font=("Verdana",10))
        self.videopanel1 = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.videopanel1.grid(row=1, column=0)

        self.player2 = None
        self.videopanel2_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        self.videopanel2_titulo.grid(row=0, column=1)

        self.bitrate_text_2 = tk.IntVar(value = 0)
        self.labelBitrate2 = tk.Label(self.videopanel2_titulo, textvariable=self.bitrate_text_2)
        self.labelBitrate2.grid(row=0, column=0)
        self.labelBitrate2.config(fg="white",bg="#602066",font=("Verdana",10))

        self.videopanel2 = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.videopanel2.grid(row=1, column=1)

        self.player3 = None
        self.videopanel3_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        self.videopanel3_titulo.grid(row=0, column=2)

        self.bitrate_text_3 = tk.IntVar(value = 0)
        self.labelBitrate3 = tk.Label(self.videopanel3_titulo, textvariable=self.bitrate_text_3)
        self.labelBitrate3.grid(row=0, column=0)
        self.labelBitrate3.config(fg="white",bg="#602066",font=("Verdana",10))

        self.videopanel3 = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.videopanel3.grid(row=1, column=2)

        self.player4 = None
        self.videopanel4_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        self.videopanel4_titulo.grid(row=2, column=0)

        self.bitrate_text_4 = tk.IntVar(value = 0)
        self.labelBitrate4 = tk.Label(self.videopanel4_titulo, textvariable=self.bitrate_text_4)
        self.labelBitrate4.grid(row=0, column=0)
        self.labelBitrate4.config(fg="white",bg="#602066",font=("Verdana",10))

        self.videopanel4 = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.videopanel4.grid(row=3, column=0)

        self.player5 = None
        self.videopanel5_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        self.videopanel5_titulo.grid(row=2, column=1)

        self.bitrate_text_5 = tk.IntVar(value = 0)
        self.labelBitrate5 = tk.Label(self.videopanel5_titulo, textvariable=self.bitrate_text_5)
        self.labelBitrate5.grid(row=0, column=0)
        self.labelBitrate5.config(fg="white",bg="#602066",font=("Verdana",10))

        self.videopanel5 = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.videopanel5.grid(row=3, column=1)

        self.player6 = None
        self.videopanel6_titulo = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_titulo_h, background="#602066")
        self.videopanel6_titulo.grid(row=2, column=2)

        self.bitrate_text_6 = tk.IntVar(value = 0)
        self.labelBitrate6 = tk.Label(self.videopanel6_titulo, textvariable=self.bitrate_text_6)
        self.labelBitrate6.grid(row=0, column=0)
        self.labelBitrate6.config(fg="white",bg="#602066",font=("Verdana",10))

        self.videopanel6 = tk.Frame(self.frame_sec_der_top, width=cam_w, height=cam_h, background="#602066")
        self.videopanel6.grid(row=3, column=2)


        # self.Instance = vlc.Instance('--input-repeat=99999')
        self.Instance = vlc.Instance()

        # direc_principal = '/home/xirioxinf/Documentos'
        configuracion = configparser.ConfigParser() # abre archivo de configuración
        configuracion.read('config/config.cfg') # lee el archivo de configuración
        cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema
        for i in range(0,int(cantidad_camaras)):
            url = 'rtsp://admin:xiriox3000@10.1.1.'+configuracion['IP']['cam'+str(i+1)]+':554'
            ip = '10.1.1.'+configuracion['IP']['cam'+str(i+1)]
            if i == 0:
                self.play1(url)
                t1 = threading.Thread(target=self.set_bitrate1) # crea el hilo
                t1.start()
                # self.set_bitrate1()
            if i == 1:
                self.play2(url)
                t2 = threading.Thread(target=self.set_bitrate2)
                t2.start()
            if i == 2:
                self.play3(url)
                t3 = threading.Thread(target=self.set_bitrate3)
                t3.start()
            if i == 3:
                self.play4(url)
                t4 = threading.Thread(target=self.set_bitrate4)
                t4.start()
            if i == 4:
                self.play5(url)
                t5 = threading.Thread(target=self.set_bitrate5)
                t5.start()
            if i == 5:
                self.play6(url)
                t6 = threading.Thread(target=self.set_bitrate6)
                t6.start()


        # self.set_bitrate1('10.1.1.71')

        #
        # url = 'rtsp://admin:xiriox3000@10.1.1.71:554'
        # self.play(self.player1,self.videopanel1,url)
        # url = 'rtsp://admin:xiriox3000@10.1.1.72:554'
        # self.play(self.player2,self.videopanel2,url)
        # url = 'rtsp://admin:xiriox3000@10.1.1.73:554'
        # self.play(self.player3,self.videopanel3,url)
        # url = 'rtsp://admin:xiriox3000@10.1.1.74:554'
        # self.play(self.player4,self.videopanel4,url)
        # url = 'rtsp://admin:xiriox3000@10.1.1.75:554'
        # self.play(self.player5,self.videopanel5,url)
        # url = 'rtsp://admin:xiriox3000@10.1.1.76:554'
        # self.play(self.player6,self.videopanel6,url)


    def play1(self,url):
        self.player1 = self.Instance.media_player_new()
        Media = self.Instance.media_new(url)
        self.player1.set_media(Media)
        self.player1.set_xwindow(self.videopanel1.winfo_id())
        if self.player1.play() == -1:
            self.errorDialog("Unable to play.")

    def play2(self,url):
        self.player2 = self.Instance.media_player_new()
        Media = self.Instance.media_new(url)
        self.player2.set_media(Media)
        self.player2.set_xwindow(self.videopanel2.winfo_id())
        if self.player2.play() == -1:
            self.errorDialog("Unable to play.")

    def play3(self,url):
        self.player3 = self.Instance.media_player_new()
        Media = self.Instance.media_new(url)
        self.player3.set_media(Media)
        self.player3.set_xwindow(self.videopanel3.winfo_id())
        if self.player3.play() == -1:
            self.errorDialog("Unable to play.")

    def play4(self,url):
        self.player4 = self.Instance.media_player_new()
        Media = self.Instance.media_new(url)
        self.player4.set_media(Media)
        self.player4.set_xwindow(self.videopanel4.winfo_id())
        if self.player4.play() == -1:
            self.errorDialog("Unable to play.")

    def play5(self,url):
        self.player5 = self.Instance.media_player_new()
        Media = self.Instance.media_new(url)
        self.player5.set_media(Media)
        self.player5.set_xwindow(self.videopanel5.winfo_id())
        if self.player5.play() == -1:
            self.errorDialog("Unable to play.")

    def play6(self,url):
        self.player6 = self.Instance.media_player_new()
        Media = self.Instance.media_new(url)
        self.player6.set_media(Media)
        self.player6.set_xwindow(self.videopanel6.winfo_id())
        if self.player6.play() == -1:
            self.errorDialog("Unable to play.")

    def stop(self,player):
        player.stop()
        # reset the time slider
        self.timeslider.set(0)

    def restart(self,player):
        if player.play() == -1:
            self.errorDialog("Unable to play.")

    def check_ping(self,ip):
        response = os.system("ping -c 1 " + ip)
        if response == 0:
            pingstatus = True
        else:
            pingstatus = False
        return pingstatus

    def set_bitrate1(self):
        configuracion = configparser.ConfigParser() # abre archivo de configuración
        configuracion.read('config/config.cfg') # lee el archivo de configuración
        ip = '10.1.1.'+configuracion['IP']['cam1']
        url = 'rtsp://admin:xiriox3000@10.1.1.'+configuracion['IP']['cam1']+':554'
        if self.check_ping(ip):
            self.bitrate_text_1.set(ip)
        else:
            self.bitrate_text_1.set('conectando...')
            self.player1.stop()
            self.play1(url)
        self.labelBitrate1.after(250, self.set_bitrate1)

    def set_bitrate2(self):
        configuracion = configparser.ConfigParser() # abre archivo de configuración
        configuracion.read('config/config.cfg') # lee el archivo de configuración
        ip = '10.1.1.'+configuracion['IP']['cam2']
        url = 'rtsp://admin:xiriox3000@10.1.1.'+configuracion['IP']['cam2']+':554'
        if self.check_ping(ip):
            self.bitrate_text_2.set(ip)
        else:
            self.bitrate_text_2.set('conectando...')
            self.player2.stop()
            self.play2(url)
        self.labelBitrate2.after(250, self.set_bitrate2)


    def set_bitrate3(self):
        configuracion = configparser.ConfigParser() # abre archivo de configuración
        configuracion.read('config/config.cfg') # lee el archivo de configuración
        ip = '10.1.1.'+configuracion['IP']['cam3']
        url = 'rtsp://admin:xiriox3000@10.1.1.'+configuracion['IP']['cam3']+':554'
        if self.check_ping(ip):
            self.bitrate_text_3.set(ip)
        else:
            self.bitrate_text_3.set('conectando...')
            self.player3.stop()
            self.play3(url)
        self.labelBitrate3.after(250, self.set_bitrate3)


    def set_bitrate4(self):
        configuracion = configparser.ConfigParser() # abre archivo de configuración
        configuracion.read('config/config.cfg') # lee el archivo de configuración
        ip = '10.1.1.'+configuracion['IP']['cam4']
        url = 'rtsp://admin:xiriox3000@10.1.1.'+configuracion['IP']['cam4']+':554'
        if self.check_ping(ip):
            self.bitrate_text_4.set(ip)
        else:
            self.bitrate_text_4.set('conectando...')
            self.player4.stop()
            self.play4(url)
        self.labelBitrate4.after(250, self.set_bitrate4)


    def set_bitrate5(self):
        configuracion = configparser.ConfigParser() # abre archivo de configuración
        configuracion.read('config/config.cfg') # lee el archivo de configuración
        ip = '10.1.1.'+configuracion['IP']['cam5']
        url = 'rtsp://admin:xiriox3000@10.1.1.'+configuracion['IP']['cam5']+':554'
        if self.check_ping(ip):
            self.bitrate_text_5.set(ip)
        else:
            self.bitrate_text_5.set('conectando...')
            self.player5.stop()
            self.play5(url)
        self.labelBitrate5.after(250, self.set_bitrate5)


    def set_bitrate6(self):
        configuracion = configparser.ConfigParser() # abre archivo de configuración
        configuracion.read('config/config.cfg') # lee el archivo de configuración
        ip = '10.1.1.'+configuracion['IP']['cam6']
        url = 'rtsp://admin:xiriox3000@10.1.1.'+configuracion['IP']['cam6']+':554'
        if self.check_ping(ip):
            self.bitrate_text_6.set(ip)
        else:
            self.bitrate_text_6.set('conectando...')
            self.player6.stop()
            self.play6(url)
        self.labelBitrate6.after(250, self.set_bitrate6)


    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        print('error')
        edialog = tk.tkMessageBox.showerror(self, 'Error', errormessage)

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"): #(1)
        Tk_get_root.root= tk.Tk()  #initialization call is inside the function
    return Tk_get_root.root

def _quit():
    print("_quit: bye")
    root = Tk_get_root()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)

if __name__ == "__main__":
    # Create a Tk.App(), which handles the windowing system event loop
    root = Tk_get_root()
    root.protocol("WM_DELETE_WINDOW", _quit)

    player = Player(root, title="XIRIOX")
    # show the player window centred and run the application
    root.configure(background='#602066')
    # style = ttk.Style()
    # style.theme_create( "st_app", parent="alt", settings={
    #     ".":             {"configure": {"background"      : "#602066",
    #                                     "foreground"      : "#602066",
    #                                     "relief"          : "flat",
    #                                     "highlightcolor"  : "#602066"}},
    #
    #     "TLabel":        {"configure": {"foreground"      : "#602066",
    #                                     "padding"         : 10,
    #                                     "font"            : ("Calibri", 12)}},
    #
    #     "TNotebook":     {"configure": {"padding"         : 5}},
    #     "TNotebook.Tab": {"configure": {"padding"         : [25, 5],
    #                                     "foreground"      : "white"},
    #                         "map"      : {"background"      : [("selected", "#602066")],
    #                                     "expand"          : [("selected", [1, 1, 1, 0])]}},
    #
    #     "TCombobox":     {"configure": {"selectbackground": "#602066",
    #                                     "fieldbackground" : "white",
    #                                     "background"      : "#602066",
    #                                     "foreground"      : "black"}},
    #
    #     "TButton":       {"configure": {"font"            :("Calibri", 13, 'bold'),
    #                                     "background"      : "black",
    #                                     "foreground"      : "#602066"},
    #                         "map"      : {"background"      : [("active", "#602066")],
    #                                     "foreground"      : [("active", 'black')]}},
    #
    #     "TEntry":        {"configure": {"foreground"      : "black"}},
    #     "Horizontal.TProgressbar":{"configure": {"background": "#602066"}}
    # })
    # style.theme_use("st_app")

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(str(sw)+'x'+str(sh))
    root.mainloop()
