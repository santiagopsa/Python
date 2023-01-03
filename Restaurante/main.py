from tkinter import *
import customtkinter

#definir el Theme de colores de CustomTkinter
customtkinter.set_appearance_mode('dark')

#definir los componentes
customtkinter.set_default_color_theme('dark-blue')

# inicializando Tkinter
aplicacion = customtkinter.CTk()

# tamano de la ventana
aplicacion.geometry('1020x630+0+0')

# evitar maximizar
aplicacion.resizable(0,0)

#titulo de la ventana
aplicacion.title('Restaurante Santiago - sistema de facturacion')

#panel superior
panel_superior = Frame(aplicacion,bd=0, relief=RIDGE)
panel_superior.pack(side=TOP)

# etiqueta titulo
etiqueta_titulo= Label(panel_superior,text='Sistema de Facturacion',
                       font=('Montserrat',30), width=30,bg='grey20',fg='white')

etiqueta_titulo.grid(row=0,column=0)



# Evitar que la pantalla se cierre
aplicacion.mainloop()