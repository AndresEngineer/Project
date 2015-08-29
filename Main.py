# Trabajando con FILES


def Archivos(string, location):

    
    #archivo = open(r'C:\Users\Andres\Desktop\remeras.txt') #Esto fué para probar con un archivo cualsea a que buscara la cedula y le diera formato

    #Esto crea el archivo de nombre Name, este archivo se ira reescribiendo a medida que lleguen cada una de las imágenes

    
    archivo = open(location + "default.txt", 'w') # 'w' es de write para crear el archivo
    archivo.close() #Cerramos el archivo para guardar
    #Aqui se edita el .txt con el parametro string que recibió la funcion
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
            if(string[cnt_2] == "-"): #Si encontró el primer guión aumentamos el flag
                flag +=1 
            elif(string[cnt_2].isdigit() == True): #Si encontró que un caracter es un digito
                flag += 1
                
            cnt_2 += 1

        if(flag > 8): #Una vez terminó el while, verificamos si encontró al menos 8 digitos o guiones
            final = "" #String vacio (para guardar el nombre)
            for char in  string: #Verificamos que se encuentren todos los digitos de la cedula
                if(char in '0123456789'): #Si el caracter es uno de estos digitos lo agregamos al string final
                    final+=char
                    if(len(final) == 3 or len(final) == 11): #Si encontró 3 digitos agregamos '-', si encontró 11 tambien formato de cedula xxx-xxxxxxx-x
                        final+= '-'
                    if(len(final) > 12): #Si hay más digitos que lo normal, nos detenemos...
                        return (final) #Retormanos el nombre (Esto se da dentro del if(si encontro mas de 8)

        cnt_1+=1



def Image(location):


    from PIL import Image #Paquete Pillow para instalar Windows: cmd -> python -m pip install Pillow
    import glob, os #Librerias Glob y Os

    size = 500,500 #Tamano en la que se exportará la imagen
    
    for infile in glob.glob("*.jpg"): #Busca todos los archivos de la ubicación actual de este script .py con la extensión *.jpg
        file = Archivos("-------------1223441221------212313---", location) # ******** Aqui debería recibir como parametro el texto generado de la imagen con pytesseract package ********
        im = Image.open(infile) # Aqui abre el archivo *.jpg
        im.thumbnail(size, Image.ANTIALIAS) # Aqui se le asigna el size a la imagen que se va a exportar
        im.save(file + ".jpg", "JPEG") #Exporta la imagen y la guarda con el nombre file que retorno el metodo Archivos


def main():

    
    string = input("Escriba la ruta en el formato C:/Ejemplo/: ")
    Image(string)
        

       

print("Opciones:")
print("0. Salir\n1.Generar archivo e imagen en la ruta actual\n2.Generar archivo e imagen en una ruta especifica\n\n")

print("Elija una opcion: ")

opcion = int(input())

if(opcion == 0):
    None
if(opcion == 1):
    Image("")
if(opcion == 2):
    main()
