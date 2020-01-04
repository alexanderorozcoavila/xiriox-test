#!/usr/bin/env python
import os
import time

while True:
	pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar.txt','w+')
	pid.write(str(os.getpid()))
	pid.close()
	os.system("python3 /home/xirioxinf/Documentos/descarte_xiriox/grabar/grabarVideos.py")
	#os.system("/home/xirioxinf/Documentos/descarte_xiriox/grabar/./grabarVideos")
	flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+')
	flag.write('0') # escribe el estado de la grabación
	flag.close()