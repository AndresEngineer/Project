"""
    Project: OCR Image process
    Project Version: 1.0
    Language: Python
    Language Version: 2.7.10
    Libraries: PIL, numpy, cv2, time, glob, os, ttk, Tkinter, pytesser Open Source
    Authors: 
            Git: AndresEngineer
            Git: Aqt01
            
            Dev: andrespengineer@gmail.com
            Dev: lowell.abbott@gmail.com
            
    This is free software, based on open source. Developed in Spanish.
    
"""

import numpy as np # Math library
import cv2 # OpenCV package from Image
from Tkinter import * # Tkinter for python GUI
import ttk #ttk from Tkinter style
from PIL import Image, ImageTk #Pillow package to install Windows: cmd -> pip install python -m Pillow
import tkFileDialog # tk File
import glob, os #Glob and Os Library
from pytesser import image_to_string, image_file_to_string # pytesser Image OCR process library
import time # Time library


# Method to Crop Image
def crop_image(name):
    
    # Readname Exception
    try:
        im = cv2.imread(name)
    except:
        x = 0
        y = 0
        w = 0
        h = 0
        return x, y, w, h
        
    #im = cv2.medianBlur(im,5) # To add blur
    hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    COLOR_MIN = np.array([10, 10, 10],np.uint8) # define color contours in range min
    COLOR_MAX = np.array([255, 255, 255],np.uint8) # define color contours in range max
    frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX) # Finding contours in range (min, max)
    imgray = frame_threshed
    ret,thresh = cv2.threshold(frame_threshed,127,255,0)
    null, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    
    # Index not found exception
    try:
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
    except:
        return 0, 0, 0, 0
        pass
    

    

    #cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2) # Trace a rectangle shape around the image


    #crop_img = im[y:y+h+5,x:x+w+5] # to Crop image

    return x, y, w, h # Return values of dimensions
   





def Function(): # Open a directory name
    import os

    os.startfile(Destino.get() + "/Procesado")
    
def Procesar():


    size = 1022, 653 #Size of image
    ErrorCount = 0 # Error Counter
    Success = 0 # Success Image
    ErrorDesconocido = 0 # Unknown error

    log = "" # Log string from Successful image process
    errorlog = "" # Log string from ERROR image process
    
    
    # Activate a button when Process is called
    botonCinco = ttk.Button(ventana, text = "Ir a la carpeta procesada", command = Function, state = ACTIVE).place(height = 30, width = 300,x = 240, y = 220)
    
    

    origen = Origen.get() # Get text from Field Origen
    destino = Destino.get() #Get text from Field destino
    
    #Exception to create a directory
    try:
        directory = destino + "/Procesado" #Intenta crear el repositorio (carpeta) si no esta creado con el nombre Procesado
        os.mkdir(directory)
        
    except:
        pass # If have lready created

    location = directory + "/" # Specifies where the images created will be saved.

    try:
        Errores = location + "Errores" # Try to create the folder where the images are stored error
        os.mkdir(Errores)
        
    except:
        pass # If have already created

    location_two = Errores + "/" # Location from Errors
    

    cnt = 1 # Rename string with errors counter to cast in advance
  
    
    # Sum of elements in directory with extensions specified (.jpg, .png, etc)
    suma = (len(glob.glob(origen + "*.jpg")) + len(glob.glob(origen + "*.png")) + len(glob.glob(origen + "*.jpeg")) + len(glob.glob(origen + "*.gif")) + len(glob.glob(origen + "*.wmp")))
    
    if(suma != 0): # If sum isn't Zero
        div = (740 / suma)  # Make a div

    # Critic Operation
    for infile in glob.glob(origen + "*.jpg") or glob.glob(origen + "*.png") or glob.glob(origen + "*.jpeg") or glob.glob(origen + "*.gif") or glob.glob(origen + "*.wmp"): #Busca todos los archivos de la ubicacion especificada con la extension *.jpg

        flag = 0 # Flag
        
        progressbar.step(div) # Progressbar 
        ventana.update() # Update master Tk
        
        # Evaluates and modifies the string to remove spaces and invalid characters in the path as Pytesser not process all the strings.
        string = EvaluarString(infile)  
        #print infile # To debug
        #print string # To debug
        
        # Rename exception, if infile equals to string
        try:
            os.rename(infile, string)
            infile = string
        except:
            pass # If infile is equals to string
        
        
        
      
        im = Image.open(infile) # Open image File
        #im.thumbnail(size, Image.ANTIALIAS) # Default size from image defined up

        x, y, w, h = crop_image(infile) # x, y, w, h get values from crop_image function return
        
        # If success exception
        if(x == 0 and y == 0 and w == 0 and h == 0):
            ErrorDesconocido += 1 # Unknown error count ++
            continue # Skip all below
        
        #im.crop((int(x+x-x*0.20)+10, y+y/2+10, w+y, h - h/4 - 40)) # Default coordinates values
        image = im.crop((x, y, w+x, y+h)) # Crop rectangle image.
        im = image # im get image value
        im.thumbnail(size, Image.ANTIALIAS) # resize image to default size defined up
        
        #im = im.crop((int(x*0.70)+10, y/2 + 10 , w , h/4 + 40)) # To debug
        #im = im.crop((294, 135, 1022, 203)) # to debug
        
        # Image crop with coordinates default
        try:
            im = im.crop((294, 100, 1022, 250))
        except:
            pass # If cant crop.
        
        # To debug, coordinates default value
        
##        x = int(x*0.70)+10 
##        y = y/2 + 10
##        w = w
##        h = h/4 + 40

        #print x, y, w, h
        
        #im = im[y: y+h/4, x+x/4:x+w+w/2]
        #cv2.imshow('Load', im)
        
        
        
        text = image_to_string(im) # Image to text with pytesseract, return a string
##        text = image_file_to_string(infile)
##        text = image_file_to_string(infile, graceful_errors=True)
       # print(text)

        
        # Here ID digits are extracted to rename the file with
        filename = Archivos(text, location) 
        
        
        if filename is None: # If cant get correct name returned
            filename = "Error" + str(cnt) # file name get name
            flag = 1 # Flag if error

        

        
        if(flag == 0): # If not error
##            T.insert(END, str(location) + str(filename) + ".jpg" + "\n") # To show in Text field
            Success+=1 # Success count increases
            T.insert(END, infile + "\n") # Show route from file in Text Field
            #cv2.imwrite(location + filename + ".jpg", image) 
            
            # Exception if cant save image
            try:
                image.save(location + filename + ".jpg")
                log+=infile+"\n"
            except:
                ErrorDesconocido+=1 # Unknown error increases
                pass 

        else: # If flag == 1, as ERROR
##            T.insert(END, str(location_two) + str(filename) + ".jpg" + "\n")
            ErrorCount += 1 # Error counter increases
            T.insert(END, infile + " # Error" + "\n" ) # Show route in textfield from error file
            #cv2.imwrite(location_two + filename + ".jpg", image) #Exporta la imagen y la guarda con el nombre file que retorno el metodo Archivos
            
            # Exception if cant save image
            try:
                image.save(location_two + filename + ".jpg")
                errorlog+=infile+"\n" # String for log
            except:
                ErrorDesconocido+=1
                pass

        cnt+=1

    Log(log, errorlog, location) # Creates a log txt file in directory
    root = Tk() # Creates a new window
    ttk.Style().configure("Button", padding = 6, relief = "flat", background = "#ccc") # Window button
    botonSalir = Button(root, text = "OK", command = root.destroy) # Exit button
    botonSalir.pack(side = BOTTOM) # Button position
    root.title("Procesamiento de Datos OCR") # Window title
    Area = Text(root, height=5, width=40) # Window size
    Area.pack(side = LEFT) # TextField place
    
    #Text area LOG
    Area.insert(END, "Imagenes Procesadas: " + str(suma) + "\nErrores: " + str(ErrorCount) +
                "\nSatisfactoriamente Procesadas: " + str(Success) + "\nSobreescritura (Repeticiones): " + str(suma - (ErrorCount + Success)) +
                "\nErroresDesconocidos: " + str(ErrorDesconocido))
                
    progressbar.stop() # Progressbar stop
    #T.config(state = "disable")
    root.mainloop()
    
    
        
def Log(log, errores,  location):
    
    
    ahora = time.strftime("%c")
    archivo = open(location + "default.txt", 'w') # Create a file named default.txt rewrite if is created
    
    # Edit txt with all writes
    archivo = open(location + "default.txt", 'a')
    archivo.write("="*50 + "\n\nFecha y hora del reporte %s"  % ahora + "\n\n" + "="*50 + "\n\n")
    archivo.write("="*50 + "\n\nSatisfactoriamente procesadas:\n\n" + "="*50 + "\n\n")
    archivo.write(log)
    archivo.write("="*50 + "\n\nErrores en procesamiento:\n\n" + "="*50 + "\n\n")
    archivo.write(errores)



        

def EvaluarString(string): #Quita los espacios del nombre del archivo de imagen


    final = ""
    t = len(string)-1
    flag = t
    cnt = 0
    value = None

##    ¡	161	u’\xa1’	\xc2\xa1	\xa1	inverted exclamation mark
##    ¿	191	u’\xbf’	\xc2\xbf	\xbf	inverted question mark
##    Á	193	u’\xc1’	\xc3\x81	\xc1	Latin capital a with acute
##    É	201	u’\xc9’	\xc3\x89	\xc9	Latin capital e with acute
##    Í	205	u’\xcd’	\xc3\x8d	\xcd	Latin capital i with acute
##    Ñ	209	u’\xd1’	\xc3\x91	\xd1	Latin capital n with tilde
##    Ó	191	u’\xbf’	\xc3\x93	\xbf	Latin capital o with acute
##    Ú	218	u’\xda’	\xc3\x9a	\xda	Latin capital u with acute
##    Ü	220	u’\xdc’	\xc3\x9c	\xdc	Latin capital u with diaeresis
##    á	225	u’\xe1’	\xc3\xa1	\xe1	Latin small a with acute
##    é	233	u’\xe9’	\xc3\xa9	\xe9	Latin small e with acute
##    í	237	u’\xed’	\xc3\xad	\xed	Latin small i with acute
##    ñ	241	u’\xf1’	\xc3\xb1	\xf1	Latin small n with tilde
##    ó	243	u’\xf3’	\xc3\xb3	\xf3	Latin small o with acute
##    ú	250	u’\xfa’	\xc3\xba	\xfa	Latin small u with acute
##    ü	252	u’\xfc’	\xc3\xbc	\xfc	Latin small u with diaeresis
    
    a = U'\xf1'
    b = U'\xa1'
    c = U'\xbf'
    d = U'\xc1'
    e = U'\xc9'
    f = U'\xcd'
    g = U'\xd1'
    h = U'\xbf'
    i = U'\xda'
    j = U'\xdc'
    k = U'\xe1'
    l = U'\xed'
    m = U'\xe9'
    n = U'\xed'
    o = U'\xf3'
    p = U'\xfa'
    q = U'\xfc'
    
    while(t > 0):
        if(string[t] in "\*"):
            value = t
            break
        t-=1

    while(cnt <= flag):

        if(cnt <= value):
            final += string[cnt]

        
        try:
            if(cnt > value and string[cnt] not in (' ',a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q)):
                final += string[cnt]
        except:
            pass

        
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
Origen.set("") #Definimos el string del campo de texto que vamos a crear
txtOrigen = Entry(ventana, textvariable = Origen).place(bordermode=OUTSIDE, height=15,width=300, x=260, y=108) #Campo de texto
Destino = StringVar()
Destino.set("")
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


    
        

    



 
