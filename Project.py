# Procesamiento OCR

import numpy as np
import cv2 
from Tkinter import *
import ttk
from PIL import Image, ImageTk #Paquete Pillow para instalar Windows: cmd -> python -m pip install Pillow
import tkFileDialog 
import glob, os #Librerias Glob y Os
from pytesser import image_to_string, image_file_to_string
# Este codigo es para guiarme...

def crop_image(name):
    
    
    im = cv2.imread(name)
    #im = cv2.medianBlur(im,5)
    hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    COLOR_MIN = np.array([10, 10, 10],np.uint8)
    COLOR_MAX = np.array([255, 255, 255],np.uint8)
    frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)
    imgray = frame_threshed
    ret,thresh = cv2.threshold(frame_threshed,127,255,0)
    null, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt=contours[max_index]

    x,y,w,h = cv2.boundingRect(cnt)

    #cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)


    crop_img = im[y:y+h+5,x:x+w+5]

    return crop_img, x, y, w, h





def Function():
    import os

    os.startfile(Destino.get() + "/Procesado")
    
def Procesar():


    size = 1800, 1200 #Tamano en la que se exportara la imagen
    
    botonCinco = ttk.Button(ventana, text = "Ir a la carpeta procesada", command = Function, state = ACTIVE).place(height = 30, width = 300,x = 240, y = 220)
    
    

    origen = Origen.get()
    destino = Destino.get()

    try:
        directory = destino + "/Procesado" #Intenta crear el repositorio (carpeta) si no esta creado con el nombre Procesado
        os.mkdir(directory)
        
    except:
        pass #Si ya esta creado, continua

    location = directory + "/" # Especifica la ruta donde se guardarÃ¡n las imagenes procesadas

    try:
        Errores = location + "Errores" #Intenta crear el repositorio (carpeta) si no esta creado con el nombre Procesado
        os.mkdir(Errores)
        
    except:
        pass #Si ya esta creado, continua

    location_two = Errores + "/"
    

    cnt = 1 #Para renombrar strings con errores
    ErrorCount = 0
    Success = 0

    suma = (len(glob.glob(origen + "*.jpg")) + len(glob.glob(origen + "*.png")) + len(glob.glob(origen + "*.jpeg")) + len(glob.glob(origen + "*.gif")) + len(glob.glob(origen + "*.wmp")))
    if(suma != 0):
        div = (740 / suma) 
    
    for infile in glob.glob(origen + "*.jpg") or glob.glob(origen + "*.png") or glob.glob(origen + "*.jpeg") or glob.glob(origen + "*.gif") or glob.glob(origen + "*.wmp"): #Busca todos los archivos de la ubicacion especificada con la extension *.jpg

        flag = 0
        
        progressbar.step(div)
        ventana.update()
        
        string = EvaluarString(infile)
        os.rename(infile, string)
        infile = string
      
        im = Image.open(infile) # Aqui abre el archivo *.jpg
        #im.thumbnail(size, Image.ANTIALIAS) # Aqui se le asigna el size a la imagen que se va a exportar
        image, x, y, w, h = crop_image(infile)
        im = image
        im = cv2.resize(im, size) 
        #im.crop((int(x+x-x*0.20)+10, y+y/2+10, w+y, h - h/4 - 40))
        im = im[y: y+h/4, x+x/4:x+w+w/2]
        cv2.imshow('Load', im)
        
        
        text = image_to_string(im)
##        text = image_file_to_string(infile)
##        text = image_file_to_string(infile, graceful_errors=True)
        
        


        filename = Archivos(text, location) # ******** Aqui deberiaa recibir como parametro el texto -> prueba generado de la imagen con pytesseract package ********
        
        
        if filename is None:
            filename = "Error" + str(cnt)
            flag = 1

        

        
        if(flag == 0):
            T.insert(END, str(location) + str(filename) + ".jpg" + "\n")
            Success+=1
            cv2.imwrite(location + filename + ".jpg", image) #Exporta la imagen y la guarda con el nombre file que retorno el metodo Archivos

        else:
            T.insert(END, str(location_two) + str(filename) + ".jpg" + "\n")
            ErrorCount += 1
            cv2.imwrite(location_two + filename + ".jpg", image) #Exporta la imagen y la guarda con el nombre file que retorno el metodo Archivos

        cnt+=1

    root = Tk() #Creamos la ventana
    ttk.Style().configure("Button", padding = 6, relief = "flat", background = "#ccc")
    botonSalir = Button(root, text = "OK", command = root.destroy)
    botonSalir.pack(side = BOTTOM)
    root.title("Procesamiento de Datos OCR") # Definimos el titulo de la ventana
    Area = Text(root, height=5, width=40)
    Area.pack(side = LEFT)
    Area.insert(END, "Imagenes Procesadas: " + str(suma) + "\nErrores: " + str(ErrorCount) + "\nSatisfactoriamente Procesadas: " + str(Success))
    progressbar.stop()
    #T.config(state = "disable")
    root.mainloop()
    
        
    

        

def EvaluarString(string): #Quita los espacios del nombre del archivo de imagen


    final = ""
    t = len(string)-1
    flag = t
    cnt = 0
    while(t > 0):
        if(string[t] in "\*"):
            value = t
            break
        t-=1

    while(cnt <= flag):

        if(cnt <= value):
            final += string[cnt]
        
        if(cnt > value and string[cnt] not in ' '):
            final += string[cnt]
        
        cnt+=1

    return(final)

    
def Archivos(string, location):


    #Esto crea el archivo de nombre Name, este archivo se ira reescribiendo a medida que lleguen cada una de las imÃƒÂ¡genes

    archivo = open(location + "default.txt", 'w') # 'w' es de write para crear el archivo
    #Aqui se edita el .txt con el parametro string que recibiÃƒÂ³ la funcion
    archivo = open(location + "default.txt", 'a')
    archivo.write(string)
    archivo = open(location + "default.txt", 'r') # Abrimos el archivo en solo lectura
    lineas = archivo.readlines() #Obtenemos todas las lineas de texto
        

    cnt_1 = 0 #Contador de lineas
    while(cnt_1 < len(lineas)): #while(cnt_1 < len(lineas)):
        
        string = lineas[cnt_1] #Asignamos a string ahora el valor de lineas en la posicion cnt_1 (recordemos que es una lista o array de strings)
        flag = 1 # Asumimos que encontro un digito de la cedula como minimo, devolvemos el valor a 1 para cada linea
        cnt_2 = 0 #Contador de cada columna del string (cada caracter que contiene)
        
        while(cnt_2 < len(string) and flag < 12): #flag < 12 porque la cedula tiene 12 caracteres o digitos
            if(string[cnt_2] == "-"): #Si encontrÃƒÂ³ el primer guiÃƒÂ³n aumentamos el flag
                flag +=1 
            elif(string[cnt_2].isdigit() == True): #Si encontramos que un caracter es un digito
                flag += 1
                
            cnt_2 += 1

        if(flag >= 9): #Una vez termina el while, verificamos si encontramos al menos 8 digitos o guiones
            final = "" #String vacio (para guardar el nombre)
            for char in  string: #Verificamos que se encuentren todos los digitos de la cedula
                if(char in '0123456789'): #Si el caracter es uno de estos digitos lo agregamos al string final
                    final+=char
                    if(len(final) == 3 or len(final) == 11): #Si encontrÃƒÂ³ 3 digitos agregamos '-', si encontrÃƒÂ³ 11 tambien formato de cedula xxx-xxxxxxx-x
                        final+= '-'
                    if(len(final) > 12):
                        break
            return str(final) #Retormanos el nombre (Esto se da dentro del if(si encontro mas de 8)

        cnt_1+=1


def Salida():

    ventana.destroy()

def DirectorioDestino():
    dirname = tkFileDialog.askdirectory(parent = ventana, initialdir = "C:/", title=('Selecciona el directorio donde se creara la carpeta'),) #La ventana para definir el directorio
    Destino.set(dirname) #Asignamos la direccion elegida al campo destino
    
    
def DirectorioOrigen():
    dirname = tkFileDialog.askdirectory(parent = ventana, initialdir = "C:/", title='Selecciona el directorio donde estan las imagenes') #La ventana para definir el directorio
    Origen.set(dirname + '/') #Asignamos la direccion elegida al campo origen


    



    
############ EL MAIN ###############
    





ventana = Tk() #Creamos la ventana
ttk.Style().configure("Button", padding = 6, relief = "flat", background = "#ccc")
ventana.geometry("740x580") #Definimos el size de la ventana
ventana.title("Procesamiento de Datos OCR") # Definimos el titulo de la ventana
ventana.resizable(0,0)



image = Image.open("Ocr.png") #Cargamos la imagen
image.thumbnail((80, 80), Image.ANTIALIAS) #Recortamos la imagen
photo = ImageTk.PhotoImage(image) #Instanciamos la imagen

label = Label(ventana, image=photo).place(x = 140, y = 10) # Creamos un label de la imagen en el frame ventana definimos la posicion x, y

ttk.Style().configure("TButton", padding=6, relief="flat",
   background="#ccc")

progressbar = ttk.Progressbar(orient=HORIZONTAL, length=740, mode='determinate')
progressbar.pack(side = BOTTOM)


ttk.Label(text="Test", style="BW.TLabel")
LabelUser = Label(text = "Optical Character Recognition", font = ("Arial Narrow", 18)).place(x = 260, y = 30) #Creamos labels de texto
LabelTwo = Label(text = "Directorio de imagenes (Origen): ", font = ("Calibri", 12)).place(x = 20, y = 100) #Creamos labels de Texto
LabelThree = Label(text = "Directorio de imagenes (Destino): ", font = ("Calibri", 12)).place(x = 20, y = 140) #Creamos labels de texto

Origen = StringVar() #Tipo String
Origen.set("C:/") #Definimos el string del campo de texto que vamos a crear
txtOrigen = Entry(ventana, textvariable = Origen).place(bordermode=OUTSIDE, height=15,width=300, x=260, y=108) #Campo de texto
Destino = StringVar()
Destino.set("C:/")
txtDestino = Entry(ventana, textvariable = Destino).place(bordermode=OUTSIDE, height=15,width=300, x=260, y=148)

##T = Text(ventana, height=15, width=90, state = "disable").place(x=5, y=280)
##scroll = Scrollbar(ventana, command=T.yview)

T = Text(ventana, height=15, width=90)
scroll = Scrollbar(ventana, command = T.yview)
T.configure(yscrollcommand=scroll.set)
T.pack(side=LEFT)
scroll.place(height = 245, x=715, y=280)
T.place(x=5, y=280)


#Creamos los botones cada uno con su funcion definida mas arriba, dentro de command
botonUno = ttk.Button(ventana, text = "Procesar",  command = Procesar).place(height = 30, width = 100,x = 270, y = 180)
botonDos = ttk.Button(ventana, text = "Salir", command = Salida).place(height = 30, width = 100,x = 400, y = 180)

#Creamos los botones cada uno con su funcion definida mas arriba, dentro de command 
botonTres = ttk.Button(ventana, text = "Examinar",  command = DirectorioOrigen).place(height = 30, width = 100,x = 570, y = 105)
botonCuatro = ttk.Button(ventana, text = "Examinar",  command = DirectorioDestino).place(height = 30, width = 100,x = 570, y = 145)


ventana.mainloop() #Llamamos al frame


    
        

    



 
