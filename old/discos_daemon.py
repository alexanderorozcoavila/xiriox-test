import os
import time
import psutil
import tkinter as tk

direcFolder = '/media/xirioxinf/'
unidades = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# intenta montar todas las unidades sda1..sdb2...etc
tiempo = 3

while True:
    time.sleep(tiempo)
    for x in range(0,len(unidades)):
        os.system('gio mount -d /dev/sd'+unidades[x])
        for z in range(1,5):
            os.system('gio mount -d /dev/sd'+unidades[x]+str(z))

    hddFolder = os.listdir(direcFolder)
    print(hddFolder)

    if "Ext1" not in hddFolder and "Ext2" not in hddFolder and "Ext3" not in hddFolder:
        tiempo = 0
        pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar.txt','r')
        pid_grabar = pid.read()
        pid.close()                                             
        pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar2.txt','r')
        pid_grabar2 = pid.read()
        pid.close()
        #print(pid_grabar, pid_encriptar)
        os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar)) # detiene el proceso de grabación
        os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar2)) # detiene el proceso de grabación
        os.system("echo xiriox3000 | sudo -S pkill -f ffmpeg")
        flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+') #crea el archivo log
        flag.write('2')
        flag.close()
        discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
        discoLleno.write('true')
        discoLleno.close()
        print("TODOS DESCONECTADOS")
        ventana = tk.Tk()
        #ventana.after(3000, lambda: ventana.destroy())
        ventana.title("Apagando Equipo")
        ventana.geometry("640x400")
        imagen = tk.PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/discos/error_todos_discos.png")
        fondo = tk.Label(ventana,image=imagen).place(x=-1,y=-1)
        ventana.wm_attributes('-type', 'splash')
        ventana.mainloop()
    elif "Ext1" not in hddFolder:
        tiempo = 0
        pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar.txt','r')
        pid_grabar = pid.read()
        pid.close()                                             
        pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar2.txt','r')
        pid_grabar2 = pid.read()
        pid.close()
        #print(pid_grabar, pid_encriptar)
        os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar)) # detiene el proceso de grabación
        os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar2)) # detiene el proceso de grabación
        os.system("echo xiriox3000 | sudo -S pkill -f ffmpeg")
        flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+') #crea el archivo log
        flag.write('2')
        flag.close()
        discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
        discoLleno.write('true')
        discoLleno.close()
        print("DISCO 1 DESCONECTADO")
        ventana = tk.Tk()
        #ventana.after(3000, lambda: ventana.destroy())
        ventana.title("Apagando Equipo")
        ventana.geometry("640x400")
        imagen = tk.PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/discos/error_disco1.png")
        fondo = tk.Label(ventana,image=imagen).place(x=-1,y=-1)
        ventana.wm_attributes('-type', 'splash')
        ventana.mainloop()
    elif "Ext2" not in hddFolder:
        tiempo = 0
        pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar.txt','r')
        pid_grabar = pid.read()
        pid.close()                                             
        pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar2.txt','r')
        pid_grabar2 = pid.read()
        pid.close()
        #print(pid_grabar, pid_encriptar)
        os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar)) # detiene el proceso de grabación
        os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar2)) # detiene el proceso de grabación
        os.system("echo xiriox3000 | sudo -S pkill -f ffmpeg")
        flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+') #crea el archivo log
        flag.write('2')
        flag.close()
        discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
        discoLleno.write('true')
        discoLleno.close()
        print("DISCO 2 DESCONECTADO")
        ventana = tk.Tk()
        #ventana.after(3000, lambda: ventana.destroy())
        ventana.title("Apagando Equipo")
        ventana.geometry("640x400")
        imagen = tk.PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/discos/error_disco2.png")
        fondo = tk.Label(ventana,image=imagen).place(x=-1,y=-1)
        ventana.wm_attributes('-type', 'splash')
        ventana.mainloop()
    elif "Ext3" not in hddFolder:
        tiempo = 0
        pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar.txt','r')
        pid_grabar = pid.read()
        pid.close()                                             
        pid = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/pid_grabar2.txt','r')
        pid_grabar2 = pid.read()
        pid.close()
        #print(pid_grabar, pid_encriptar)
        os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar)) # detiene el proceso de grabación
        os.system('echo xiriox3000 | sudo -S kill -9 '+str(pid_grabar2)) # detiene el proceso de grabación
        os.system("echo xiriox3000 | sudo -S pkill -f ffmpeg")
        flag = open('/home/xirioxinf/Documentos/descarte_xiriox/grabar/grabar','w+') #crea el archivo log
        flag.write('2')
        flag.close()
        discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
        discoLleno.write('true')
        discoLleno.close()
        print("DISCO 2 DESCONECTADO")
        ventana = tk.Tk()
        #ventana.after(3000, lambda: ventana.destroy())
        ventana.title("Apagando Equipo")
        ventana.geometry("640x400")
        imagen = tk.PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/discos/error_disco3.png")
        fondo = tk.Label(ventana,image=imagen).place(x=-1,y=-1)
        ventana.wm_attributes('-type', 'splash')
        ventana.mainloop()
    else:
        tiempo = 3
        discoLleno = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/sinDiscos.txt', 'w')
        discoLleno.write('false')
        discoLleno.close()

    print(tiempo)

"""while True:
    time.sleep(2)
    for x in range(0,len(unidades)):
        os.system('gio mount -d /dev/sd'+unidades[x])
        dps = psutil.disk_partitions()
        for i in dps:
            if i[0] == '/dev/sd'+unidades[x]:
                nombre_hdd = psutil.disk_usage(i[1])
                if nombre_hdd[0] <  3500397795328:
                    os.system('echo xiriox3000 | sudo -S umount '+i[0])
                    time.sleep(0.5)
        for z in range(1,8):
            os.system('gio mount -d /dev/sd'+unidades[x]+str(z))
            dps = psutil.disk_partitions()
            for i in dps:
                if i[0] == '/dev/sd'+unidades[x]+str(z):
                    nombre_hdd = psutil.disk_usage(i[1])
                    if nombre_hdd[0] <  3500397795328:
                        os.system('echo xiriox3000 | sudo -S umount '+i[0])
                        time.sleep(0.5)

    hddFolder = os.listdir(direcFolder)
    print(hddFolder)"""