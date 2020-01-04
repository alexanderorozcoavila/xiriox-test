#!/usr/bin/env python
import os
import time
import sys

time.sleep(6)

while True:
    print(os.getpid())
    pid = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/pid_encriptar.txt','w+')
    pid.write(str(os.getpid()))
    pid.close()
    os.system("echo xiriox3000 | sudo -S /home/xirioxinf/Documentos/descarte_xiriox/encriptar/./encriptar")
    #os.system("echo xiriox3000 | python3 /home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptar.py")
    print('sale')
    """flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','r') #crea el archivo log
    estado_encriptar = flag.read()
    flag.close()
    print(estado_encriptar)
    if estado_encriptar == '2':
        print("Termina por apagado")
        sys.exit()"""
