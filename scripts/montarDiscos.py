import configparser
import os

configuracion = configparser.ConfigParser() # abre archivo de configuración
configuracion.read('/home/xirioxinf/Documentos/descarte_xiriox/config/config.cfg') # lee el archivo de configuración
#dir_main = cantidad_camaras = configuracion['Directorios']['dir_main'] # cantidad de cámaras para el sistema

ext1 = configuracion["Externos"]["Ext1"]
ext2 = configuracion["Externos"]["Ext2"]
ext3 = configuracion["Externos"]["Ext3"]

#echo xiriox3000 | sudo -S veracrypt -t -k "" -p xiriox3000 --pim=0 --protect-hidden=no /dev/sdf2 /tmp/Ext2
print(ext1, ext2, ext3)

if ext1 != "":
    os.system('echo xiriox3000 | sudo -S veracrypt -t -k "" -p xiriox3000 --pim=0 --protect-hidden=no /dev/'+ext1+' /home/xirioxinf/Ext1')
    print(ext1)
if ext2 != "":
    os.system('echo xiriox3000 | sudo -S veracrypt -t -k "" -p xiriox3000 --pim=0 --protect-hidden=no /dev/'+ext2+' /home/xirioxinf/Ext2')
    print(ext2)
if ext3 != "":
    os.system('echo xiriox3000 | sudo -S veracrypt -t -k "" -p xiriox3000 --pim=0 --protect-hidden=no /dev/'+ext3+' /home/xirioxinf/Ext3')
    print(ext3)

