import PySimpleGUI as sg
from datetime import datetime
import subprocess
import configparser
import configparser, time, sys, os

sg.change_look_and_feel('DarkBlue')
# All the stuff inside your window.
layout = [  [sg.Text('Sistema de Instalación DRI')],
            [sg.Text('Ingrese clave root',size=(30, 1)), sg.InputText()],
            [sg.Text('Ingrese cantidad de camaras',size=(30, 1)), sg.InputText()],
            [sg.Text('Ingrese DRI-ID',size=(30, 1)), sg.InputText()],
            [sg.Text('Ingrese EMBARCACION-ID',size=(30, 1)), sg.InputText()],
            [sg.Button('Instalar'), sg.Button('Cancelar')] ]

# Create the Window
window = sg.Window('Install DRI', layout)
# Event Loop to process "events" and get the "values" of the inputs
def install():
    if values[0] is None:
        sg.Popup("Ingrese los valores de los campos.")
    else:
        pwd = values[0]
        cam = values[1]
        id_dri = values[2]
        id_embarcacion = values[3]
        # sg.Popup('El sistema requiere reiniciarse, haga clic en OK')
        os.system("echo "+pwd+" | sudo -S mkdir /home/xirioxinf/Ext1")
        os.system("echo "+pwd+" | sudo -S mkdir /home/xirioxinf/Ext2")
        os.system("echo "+pwd+" | sudo -S mkdir /home/xirioxinf/Ext3")
        os.system("echo "+pwd+" | sudo -S chmod 777 -R /home/xirioxinf/Ext1")
        os.system("echo "+pwd+" | sudo -S chmod 777 -R /home/xirioxinf/Ext2")
        os.system("echo "+pwd+" | sudo -S chmod 777 -R /home/xirioxinf/Ext3")
        
        configuracion = configparser.ConfigParser() # abre archivo de configuraci贸n
        configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg')
        configuracion['Videos']['cantidad_camaras'] = cam
        configuracion['ID']['id_dri'] = id_dri
        configuracion['ID']['id_embarcacion'] = id_embarcacion
        with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
            configuracion.write(configfile)
        # os.system("echo "+pwd+" | sudo -S apt install xfce4")
        os.system("mkdir /home/xirioxinf/.config/autostart")
        os.system("rm /home/xirioxinf/.config/autostart/EJECUTAR.desktop")
        os.system("cp /home/xirioxinf/Documentos/descarte_xiriox/config-os/EJECUTAR.desktop /home/xirioxinf/.config/autostart/EJECUTAR.desktop")
        os.system("echo "+pwd+" | sudo -S rm /var/lib/AccountsService/users/xirioxinf")
        os.system("echo "+pwd+" | sudo -S cp /home/xirioxinf/Documentos/descarte_xiriox/config-os/xirioxinf /var/lib/AccountsService/users/xirioxinf")
        os.system("echo "+pwd+" | sudo -S timedatectl set-timezone Europe/London")

        # os.system("echo "+pwd+" | sudo -S dpkg libwxbase3.0-0v5_3.0.4+dfsg-3_amd64.deb")
        # os.system("echo "+pwd+" | sudo -S dpkg libwxgtk3.0-gtk3-0v5_3.0.4+dfsg-3_amd64.deb")
        # os.system("echo "+pwd+" | sudo -S dpkg veracrypt-console-1.24-Hotfix1-Ubuntu-18.04-amd64.deb")
        # os.system("pip3 install -r /home/xirioxinf/Documentos/descarte_xiriox/config-os/librerias.txt")
        os.system("echo "+pwd+" | sudo -S chmod 777 -R /media/xirioxinf")
        os.system("echo "+pwd+" | sudo -S rm /usr/share/backgrounds/xfce/xfce-teal.jpg")
        os.system("echo "+pwd+" | sudo -S cp /home/xirioxinf/Documentos/descarte_xiriox/config-os/background.png /usr/share/backgrounds/xfce/")
        os.system("echo "+pwd+" | sudo -S mv /usr/share/backgrounds/xfce/background.png /usr/share/backgrounds/xfce/xfce-teal.jpg")

        sg.Popup("El sistema requiere reiniciarse, haga clic en OK")
        os.system("echo "+pwd+" | sudo -S reboot")

while True:
    event, values = window.read()
    if event in (None, 'Cancelar'):   # if user closes window or clicks cancel
        break
    if event in (None, 'Instalar'):   # if user closes window or clicks cancel
        install()
    # print('You entered ', values[0])

window.close()
