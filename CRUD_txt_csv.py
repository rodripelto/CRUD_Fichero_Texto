import os
import datetime
def clear(): #También la podemos llamar cls (depende a lo que estemos acostumbrados)
    if os.name == "posix":
        os.system ("clear")
    elif os.name in ("ce", "nt", "dos"):
        os.system ("cls")
clear()
# De momento no lo uso pero seria para obtener la ruta donde se esta ejecutando el programa
def obtener_ruta():
    return  os.path.dirname(os.path.realpath(__file__))
# Definimos como constante donde tenemos el fichero guardado
def FICHERO():
    return obtener_ruta() + r"\Empleados.txt"
    #return r"..\Programacion\Proyectos Phyton\Pruebas\Empleados.txt"
# Generamos el menú de opciones
def menu():
    opcion=""
    while opcion not in [str(x) for x in range(1,6)] : #("1","2","3","4","5"):
        clear() # Para borrar el terminal en windows
        print("1.....Mostrar datos","2.....Añadir Datos","3.....Modificar","4.....Borrar","5.....Salir",sep="\n")
        opcion=input("Seleccione una opción y pulse enter: ")
    return opcion
# Menu para las opciones de modificar
def menu_modificar():
    opcion=""
    while True:
        while opcion not in [str(x) for x in range(1,7)] : #("1","2","3","4","5","6"):
            clear() # Para borrar el terminal en windows
            print("1.....Modificar Nombre","2.....Modificar Apellido",
            "3.....Modificar Fecha","4.....Modificar Cargo","5.....Modificar Sueldo","6.....Menú principal",sep="\n")
            opcion=input("Seleccione una opción y pulse enter: ")
        modificar(opcion)
        if opcion == "6": 
            break 
        else: opcion = ""
# Pedimos el nombre
def pedir_nombre():
    return input("Introduzca el nombre: ").capitalize()
# Pedimos el apellido
def pedir_apellido():
    return input("Introduzca el apellido: ").capitalize()
# Pedimos fecha de ingreso
def pedir_fecha():
    while True:
        fecha = (input("Introduzca fecha de ingreso, con formato dd/mm/aaaa: "))
        try:
            # Cualquier fecha incorrecta producira un error ya sea por no existir el indice
            # o error de la libreria por no poder crear el objeto
            confecha = fecha.split("/")
            datetime.datetime(int(confecha[2]),int(confecha[1]),int(confecha[0]))
            break
        except:
            print ("La fecha introducida no es correcta, intentelo de nuevo")

    return fecha
# Pedimos el cargo
def pedir_cargo():
    return input("Introduce su cargo: ").capitalize()
# Pedimos sueldo
def pedir_sueldo():
    while True:
        try:
            sueldo = float(input("Introduce el sueldo bruto: "))
            break
        except:
            print("El sueldo tiene que ser un número")
    return sueldo
# Calculamos descuento
def calcular_descuento(sueldo):
    des = 0
    if sueldo > 1800:
        des = 10
    return des
# Calculamos sueldo neto
def calcular_sueldo_neto(sueldo,descuento):
    return sueldo - (sueldo * descuento / 100)
# Agregamos los datos al fichero
def agregar():
    nregistros = str (obtener_id()+ 1)
    id = "E" + "0" * (4 - len(nregistros)) + nregistros
    nombre = pedir_nombre()
    apellido = pedir_apellido()
    fecha = pedir_fecha()
    cargo = pedir_cargo()
    sueldo = pedir_sueldo()
    descuento = calcular_descuento(sueldo)
    sueldoneto = calcular_sueldo_neto(sueldo,descuento)
    escribir_txt(((id,nombre,apellido,fecha,cargo,str(sueldo),str(descuento),str(sueldoneto)),),"a")
    modificar_id()
# Escribimos en el fichero, dependiendo del modo que enviemos añadirá o generara uno nuevo
def escribir_txt(elementos_escritura, modo="a"):
    with open(FICHERO(),mode=modo,encoding="utf-8") as fichero:
    # Escribo en el fichero un registro por fila, datos separados por ;
        for elemento in elementos_escritura:
            if len(elemento) >1 :
                datos = ";".join(elemento)
            else :
                datos = elemento
            fichero.write(datos + "\n")
# Leo el fichero de datos
def leer_fichero():
    lista= []
    with open(FICHERO(),mode="r",encoding="utf-8") as fichero:
        lineas = fichero.readlines()
        lista.append(lineas[0].replace("\n",""))
        for i in range(1,len(lineas)):
            # Elimino el salto de linea
            linea = lineas[i].replace("\n","")
            # Separo los datos y se crea una lista, ya lo podría usar así   
            datos = linea.split(";")
            lista.append(datos)
    return lista
#Imprime la información del fichero
def imprimir_fichero():
    lista = leer_fichero()
    for i in range(1,len(lista)):
        print("Id:",lista[i][0],"Nombre:",lista[i][1],"Apellido:",lista[i][2],"Fecha ingreso:",lista[i][3],
        "Cargo:",lista[i][4],"Sueldo bruto:",lista[i][5],"Descuento:",lista[i][6],"%","Sueldo neto:",
        lista[i][7],"\n")
# Modificar los datos
def modificar(opcion):
    if opcion == "6" : return # Si es la opción 6 retorna sin hacer nada, es la opción de volver al menú principal
    imprimir_fichero()
    nombre_mostrar= input("Pon un nombre de la lista: ").capitalize()
    # Compruebo si existe el nombre a buscar, si existe muesto los datos y si no existe muestro mensaje de que no existe
    lista= leer_fichero()
    opciones = {"1":pedir_nombre,"2":pedir_apellido,"3":pedir_fecha,"4":pedir_cargo,"5":pedir_sueldo}
    for registro in lista:
      if nombre_mostrar in registro:
            registro[int(opcion)] = opciones[opcion]()
            # Si se ha elegido modificar sueldo tambien hay que modificar el descuento y el sueldo neto
            if opcion == "5":
                # El registro 6 contiene el descuento y el registro 5 el sueldo
                registro[6] = calcular_descuento(registro[5])
                # El registro 7 contiene el sueldo neto.
                registro[7] = calcular_sueldo_neto(registro[5],registro[6])
                registro[5] = str(registro[5])
                registro[6] = str(registro[6])
                registro[7] = str(registro[7])
            escribir_txt(lista,"w")
            break # Rompo el bucle y no se ejecuta el else
    else: # Solo se ejecuta si se recorre la lista completa y no se rompe el bucle con break
        print("Nombre no disponible")
# Borramos un registro
def borrar():
    imprimir_fichero()
    nombre_mostrar= input("Pon un nombre de la lista: ").capitalize()
    # Compruebo si existe el nombre a buscar, si existe muesto los datos y si no existe muestro mensaje de que no existe
    lista= leer_fichero()
    for registro in lista:
      if nombre_mostrar in registro:
            seguro = input("¿Estas seguro de borrar este registro? S/N: ").upper()
            if seguro == "S" or seguro =="SI":
                lista.remove(registro)
                escribir_txt(lista,"w")
            break # Rompo el bucle y no se ejecuta el else
    else: # Solo se ejecuta si se recorre la lista completa y no se rompe el bucle con break
        print("Nombre no disponible")
# Obtener Id
def obtener_id():
    try:
        with open(FICHERO(),mode="r+",encoding="utf-8") as fichero:
            id = fichero.readlines()
            id = int (id[0])
    except:
        # Si no existe el fichero dara error entonces creamos el fichero y dara error si la primera linea no es número
        with open(FICHERO(),mode="w",encoding="utf-8") as fichero:
            fichero.write(str(0) + "\n")
            id = 0
    return id
# Modificar el Id
def modificar_id():
    id = obtener_id()
    lista = leer_fichero()
    id = id + 1
    lista[0] = str(id)
    escribir_txt(lista,"w")
# Programa principal
def main():
    opcion =""
    funciones = {"1":imprimir_fichero,"2":agregar,"3":menu_modificar,"4":borrar}
    if obtener_id() == 0:
        print ("Fichero inexistente o dañado, genere nuevos registros")
        agregar()
    while (opcion := menu()) !="5":
        funcion = funciones[opcion]
        funcion()
        if opcion !="3":
            input ("Pulsa enter para volver al menú ")

main()
