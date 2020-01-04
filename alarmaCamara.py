from tkinter import *
import time

time.sleep(15)

def leerDato(archivoTxt):
	try:
		dato = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/'+archivoTxt+'.txt', 'r')
		datoLeido = dato.read()
		dato.close()
		return datoLeido
	except Exception as e:
		print(e)



while True:
	estado = leerDato('alarmaCamara')
	if estado == 'true':
		print('Alarma de cámara')
		ventana = Tk()
		ventana.after(5000, lambda: ventana.destroy())
		ventana.title("Apagando Equipo")
		ventana.geometry("400x240")
		imagen = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/alarmaCamara.png")
		fondo = Label(ventana,image=imagen).place(x=-1,y=-1)

		ventana.wm_attributes('-type', 'splash')
		ventana.mainloop()
	else:
		print('No hay alarma de cámara')
	time.sleep(1)
		
