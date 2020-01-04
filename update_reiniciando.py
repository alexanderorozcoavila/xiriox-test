from tkinter import *

ventana = Tk()
#ventana.after(45000, lambda: ventana.destroy())
ventana.title("Reiniciando Equipo")
ventana.geometry("640x400")
imagen = PhotoImage(file="/media/xirioxinf/ORAC_UPDATE/recursos/reiniciando.png")
fondo = Label(ventana,image=imagen).place(x=-1,y=-1)
ventana.wm_attributes('-type', 'splash')
ventana.wm_attributes("-topmost", True)
#ventana.wm_attributes("-fullscreen", True)
ventana.mainloop()
print("asdasd")
#ventana2 = Tk()