# -*- coding: utf-8 -*-
#!/usr/bin/python
import tkinter as tk
from datetime import datetime, timedelta, time
import time, os
from time import gmtime

version = "v1.0.0"

global ajuste # variable global para indicar en qué GMT se encuentra
ajuste = time.strftime("%Z") # lee el GMT actual

# array con todas las horas del día
gtm = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]

#lee la fecha y hora actuales para mostrar en pantalla
def Date_secondsnow():
    global ajuste
    fecha = time.strftime("%d/%m/%Y") # lee la fecha actual
    hora = time.strftime(":%M:%S", gmtime()) # lee la hora actual, sin la hora, sólo minutos y segundos en UTC
    hora_aux = time.strftime("%H", gmtime()) # lee la hora en UTC
    #lee la posición que se encuentra la hora en UTC y le resta el GMT establecido para encontrar la hora
    # en el array gtm, con eso se determina la hora actual
    hour = gtm[gtm.index(hora_aux)+int(ajuste)] 
    #retorna la fecha y hora actuales
    return "Fecha: "+fecha+"    Hora: "+str(hour)+str(hora)+" GMT "+str(ajuste)

def set_date(): # actualiza los datos cada 250ms
    date_seconds.set(Date_secondsnow())
    labelQuestion.after(250, set_date)

def utc_invierno(): # cambia el GMT a -4 (invierno)
    global ajuste
    ajuste = "-04"
    os.system("echo xiriox3000 | sudo -S timedatectl set-timezone America/La_Paz")

def utc_verano(): # cambia el GMT a -3 (verano)
    global ajuste
    ajuste = "-03"
    os.system("echo xiriox3000 | sudo -S timedatectl set-timezone America/Argentina/Buenos_Aires")

window=tk.Tk()
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
ventana_x = 400
ventana_y = 200
x = (sw - ventana_x)/2
y = (sh - ventana_y)/2
#ventana.geometry('600x400+1+1')
window.geometry(str(ventana_x)+'x'+str(ventana_y)+'+%d+%d' % (x,y))
#window.geometry("400x200+100+100")
window.title("Cambio Horario "+version)
window.resizable(width=False, height=False)#No se puede cambiar tamaño ventana
#imagen = tk.PhotoImage(file="/home/xirioxinf/Documentos/recursos/reiniciando.png")
#fondo = tk.Label(window,image=imagen).place(x=-1,y=-1)


frame = tk.Frame(window)

date_seconds = tk.IntVar(value = 0)
state = tk.BooleanVar(value = False)

labelQuestion = tk.Label(frame, textvariable=date_seconds, padx=20, font=("Agency FB", 12))
labelQuestion.grid(row=0, column=0, sticky=tk.W)

frame.grid_rowconfigure(1, minsize=10)
frame.place(x=0,y=15)

btnSave=tk.Button(window, text="Invierno GMT -4", command=utc_invierno, font=("Agency FB", 12))
btnSave.place(x=20,y=100)

btnStop=tk.Button(window, text="Verano GMT -3", command=utc_verano, font=("Agency FB", 12))
btnStop.place(x=230,y=100)

set_date()
window.mainloop()