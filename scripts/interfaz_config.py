import PySimpleGUI as sg
from datetime import datetime
import subprocess
import configparser
import os

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
cantidad_camaras = configuracion['Videos']['cantidad_camaras'] # cantidad de cámaras para el sistema
dir_main = configuracion['Directorios']['dir_main'] # cantidad de cámaras para el sistema

# Se le da formato a los discos creando partición GPT y en NTFS
def inicializarDisco(disco):
    os.system("echo xiriox3000 | sudo -S parted /dev/"+disco+" mklabel gpt")
    print("1 Listo")
    os.system("echo xiriox3000 | sudo -S parted /dev/"+disco+" mkpart primary ntfs 0% 100%")
    print("2 Listo")
    os.system("echo xiriox3000 | sudo -S mkfs.ntfs -Q -L ext"+disco+"1 /dev/"+disco+"1 -s 4096")
    print("3 Listo")
    
# Se cifra el disco con Veracrypt
def veracrypt(disco):
    os.system('echo xiriox3000 | sudo -S veracrypt -t -c --quick --volume-type=normal /dev/'+disco+'1 --encryption=aes --hash=sha-512 --filesystem=ntfs -p xiriox3000 --pim=0 -k "" --random-source=/dev/urandom')
    print("veracrypt listo")

# analiza los discos disponibles en el sistema y los filtra hasta quedar solamente con los externos a formatear
def recDiscos():
    array = []
    try:
        test1 = subprocess.check_output("echo xiriox3000 | sudo -S sudo lsblk -fm | grep sd", shell=True)
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
        print("\n")
        var_sdx = []
        for discos in array:
            if "T" in discos[1] or "ntfs" in discos[1] and "Int1" not in discos and "Int2" not in discos and "Int3" not in discos:
                try:
                    if len(discos[0]) == 3:
                        var_sdx.append(discos[0])
                except:
                    print("error")
            print("VARIABLE ", var_sdx)
    except Exception as e:
        print(e)
        pass
    return var_sdx

sg.ChangeLookAndFeel('Reddit')
discos= recDiscos() # se obtienen los discos

urls = [] # número para cada cámara en la conexión RTSP
for i in range(0,6):
    urls.append(configuracion['IP']['cam'+str(i+1)])

try:
    columna1 = [sg.Text('Nombre ubicación de disco 1'), sg.InputText(discos[0])]
except:
    columna1 = [sg.Text('No hay disco 1'), sg.InputText("--")]
try:
    columna2 = [sg.Text('Nombre ubicación de disco 2'), sg.InputText(discos[1])]
except:
    columna2 = [sg.Text('No hay disco 2'), sg.InputText("--")]
try:
    columna3 = [sg.Text('Nombre ubicación de disco 3'), sg.InputText(discos[2])]
except:
    columna3 = [sg.Text('No hay disco 3')]

# Layout pestaña discos duros
discosLayout = [      
    [sg.Text('Formatear Discos Duros', size=(30, 1), font=("Helvetica", 25))], 
    columna1,
    columna2,
    columna3,            
    [sg.Text('_'  * 80)],          
    [sg.Submit("Guardar"), sg.Cancel("Cancelar")]      
]
# Layout pestaña configuración de cámaras
camarasLayout = [
    [sg.Text('Cantidad de cámaras'), sg.InputText(cantidad_camaras, key="_cantCamaras_")],
    [sg.Text('_'  * 80)], 
    [sg.Text('IP Cámara 1'), sg.InputText(urls[0], key="_CAM1_")],
    [sg.Text('IP Cámara 2'), sg.InputText(urls[1], key="_CAM2_")],
    [sg.Text('IP Cámara 3'), sg.InputText(urls[2], key="_CAM3_")],
    [sg.Text('IP Cámara 4'), sg.InputText(urls[3], key="_CAM4_")],
    [sg.Text('IP Cámara 5'), sg.InputText(urls[4], key="_CAM5_")],
    [sg.Text('IP Cámara 6'), sg.InputText(urls[5], key="_CAM6_")],
    [sg.Submit("Guardar"), sg.Cancel("Cancelar")]   
]
# Layout principal
layout = [[sg.TabGroup([[sg.Tab('Discos Duros', discosLayout), sg.Tab('Cámaras', camarasLayout)]])]]

window = sg.Window('Configuración Oraculus DRI', default_element_size=(40, 1)).Layout(layout)

while True:
    button, values = window.Read() # Se leen los valores de toda la ventana
    # Si se presiona alguno de los botones cancelar se cierra la aplicación
    if button == "Cancelar" or button == "Cancelar1" or button == None:
        break
    # Se presiona el botón guardar de la pestaña discos duros
    if button == "Guardar":
        for var in range(0,len(discos)):
            #print("echo xiriox3000 | sudo -S parted /dev/"+values[var]+" mklabel gpt")
            inicializarDisco(values[var])
            veracrypt(values[var])
            configuracion['Externos']['Ext'+str(var+1)] = values[var]+"1" # cantidad de cámaras para el sistema
            print('Ext'+str(var+1))
        with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
            configuracion.write(configfile)
        print("Guardado")
    # Se presiona el botón guardar de la pestaña cámaras
    if button == "Guardar0":
        print(values)
        for cam in range(0,6):
            configuracion['IP']['cam'+str(cam+1)] = values["_CAM"+str(cam+1)+"_"]

        configuracion['Videos']['cantidad_camaras'] = values['_cantCamaras_']
        with open('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg', 'w') as configfile:
            configuracion.write(configfile)
    print(button, values["_CAM3_"])

window.Close() # Cierra la ventana