#!/usr/bin/env python
import os
import time

while True:
    pid = open('/home/xirioxinf/Documentos/descarte_xiriox/encriptar/pid_encriptar.txt','w+')
    pid.write(str(os.getpid()))
    pid.close()
    os.system("python3 /home/xirioxinf/Documentos/descarte_xiriox/encriptar/encriptarVideos.py")
    #os.system("echo xiriox3000 | sudo -S /home/xirioxinf/Documentos/descarte_xiriox/encriptar/./encriptar")
    print('sale')
