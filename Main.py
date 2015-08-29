# Trabajando con FILES

"""
    # Para probarlo, se debe crear una carpeta con imagenes, cambiar la ruta en la funcion Image() como indica los comments #
    
"""
    


def Archivos(string, location):

    
    #archivo = open(r'C:\Users\Andres\Desktop\remeras.txt') #Esto fuÃ© para probar con un archivo cualsea a que buscara la cedula y le diera formato

    #Esto crea el archivo de nombre Name, este archivo se ira reescribiendo a medida que lleguen cada una de las imÃ¡genes

    
    archivo = open(location + "default.txt", 'w') # 'w' es de write para crear el archivo
    archivo.close() #Cerramos el archivo para guardar
    #Aqui se edita el .txt con el parametro string que recibiÃ³ la funcion
    archivo = open(location + "default.txt", 'a')
    archivo.write(string)
    archivo.close() #Cerramos el archivo para guardar
    archivo = open(location + "default.txt", 'r') # Abrimos el archivo en solo lectura
    lineas = archivo.readlines() #Obtenemos todas las lineas de texto
    
        

    cnt_1 = 0 #Contador de lineas
    while(cnt_1 < len(lineas)):
        
        string = lineas[cnt_1] #Asignamos a string ahora el valor de lineas en la posicion cnt_1 (recordemos que es una lista o array de strings)
        flag = 1 # Asumimos que encontro un digito de la cedula como minimo, devolvemos el valor a 1 para cada linea
        cnt_2 = 0 #Contador de cada columna del string (cada caracter que contiene)
        
        while(cnt_2 < len(string) and flag < 12): #flag < 12 porque la cedula tiene 12 caracteres o digitos
            if(string[cnt_2] == "-"): #Si encontrÃ³ el primer guiÃ³n aumentamos el flag
                flag +=1 
            elif(string[cnt_2].isdigit() == True): #Si encontrÃ³ que un caracter es un digito
                flag += 1
                
            cnt_2 += 1

        if(flag > 8): #Una vez terminÃ³ el while, verificamos si encontrÃ³ al menos 8 digitos o guiones
            final = "" #String vacio (para guardar el nombre)
            for char in  string: #Verificamos que se encuentren todos los digitos de la cedula
                if(char in '0123456789'): #Si el caracter es uno de estos digitos lo agregamos al string final
                    final+=char
                    if(len(final) == 3 or len(final) == 11): #Si encontrÃ³ 3 digitos agregamos '-', si encontrÃ³ 11 tambien formato de cedula xxx-xxxxxxx-x
                        final+= '-'
                    if(len(final) > 12): #Si hay mÃ¡s digitos que lo normal, nos detenemos...
                        return str(final) #Retormanos el nombre (Esto se da dentro del if(si encontro mas de 8)

        cnt_1+=1



def Image():


    from PIL import Image #Paquete Pillow para instalar Windows: cmd -> python -m pip install Pillow
    import glob, os #Librerias Glob y Os

    size = 500,500 #Tamano en la que se exportara la imagen

    #################################################################################
    
    # En esta direccion se debe poner ruta original donde se va a crear la carpeta  #
    
    #################################################################################

    try:
        directory = (r'C:/Users/Andres/Desktop/Testing') #Intenta crear el repositorio
        os.mkdir(directory)
    except:
        pass #Si ya esta creado, continua

    location = directory + "/" # Especifica la ruta donde se guardarán las imagenes procesadas

    #Esto es para probar cuando tengamos generado el texto de la cedula, lo usamos para que pueda ver todas las JPG de la carpeta
    prueba = "000--0102-0031-3813" #Este deberia ser el texto generado
    GeneraString(prueba) #Probando para que cada cedula sea diferente (Esto no va)
    
    ##########################################################################################################
    
    # En esta direccion del glob se debe poner ruta original donde estan almacenando las imagenes a procesar #
    
    ##########################################################################################################
    
    for infile in glob.glob("C:/Users/Andres/Desktop/Imagenes/*.jpg"): #Busca todos los archivos de la ubicacion especificada con la extension *.jpg
        
        filename = Archivos(prueba, location) # ******** Aqui deberiaa recibir como parametro el texto -> prueba generado de la imagen con pytesseract package ********
        im = Image.open(infile) # Aqui abre el archivo *.jpg
        #im.thumbnail(size, Image.ANTIALIAS) # Aqui se le asigna el size a la imagen que se va a exportar
        
        try:
            region = im.crop((0,0,500,500)) #Recorta la imagen a 500 x 500 Pix
        except:
            pass
        
        region.save(location + filename + ".jpg", "JPEG") #Exporta la imagen y la guarda con el nombre file que retorno el metodo Archivos
        prueba = GeneraString(prueba)


def GeneraString(prueba):

    import random

    l = list(prueba)
    random.shuffle(l)
    result = ''.join(l)
    return (result)
    
        

    



 
