from tkinter import *
import time

def leerDato(archivoTxt):
	try:
		dato = open('/home/xirioxinf/Documentos/descarte_xiriox/alarmas/'+archivoTxt+'.txt', 'r')
		datoLeido = dato.read()
		dato.close()
		return datoLeido
	except Exception as e:
		print(e)



while True:
	estado = leerDato('upsFuncionando')
	if estado == 'true':
		ventana = Tk()
		ventana.after(5000, lambda: ventana.destroy())
		ventana.title("Apagando Equipo")
		ventana.geometry("400x240")
		imagen = PhotoImage(file="/home/xirioxinf/Documentos/descarte_xiriox/img/alarmaUPS.png")
		fondo = Label(ventana,image=imagen).place(x=-1,y=-1)
		#boton = Button(ventana, text="Apagar Equipo", command=funcion)
		#boton.place(x = 135, y = 200)
		ventana.wm_attributes('-type', 'splash')
		ventana.mainloop()
	else:
		print('No hay alarma de cámara')
	time.sleep(1)
		
