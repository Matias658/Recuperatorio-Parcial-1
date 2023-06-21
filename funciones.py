import os
import re
import json
import random
# El programa debe ofrecer un menú con las siguientes opciones:
# Cargar datos desde archivo:
# Listar cantidad por marca:
# Listar insumos por marca:
# Buscar insumo por característica:
# Listar insumos ordenados:
# Realizar compras:
# Guardar en formato JSON:
# Leer desde formato JSON:
# Actualizar precios:
# Salir del programa
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#*************************************************FUNCIONES PRINCIPALES****************************************************************
#Cargar datos y mostrarlos
def leer_csv(path:str, opcion:bool):
    """Lee el .csv y agrega todo lo que contiene en una lista

    Args:
        path (str): Ruta a ingresar
        opcion (bool): True para hacer cambios. False para no cambiar nada

    Returns:
        list: 
    """
    lista = []
    with open(path, 'r', encoding="utf8") as archivo:   #encoding="utf8" fue la única solución que pude encontrar sobre el error de librerías que mi tiraba. Lo encontré en la página de https://stackoverflow.com
        for elemento in archivo:
            elemento = elemento.replace("\n", "")   #elimino los \n al final de cada linea del csv
            elemento = elemento.replace("~", " | ")
            elemento = elemento.replace("$", "")
            lista_aux = elemento.split(',') 
            lista.append(lista_aux) #armo una lista por cada linea 
        if opcion:  #puse esto en caso de que otro .csv no lo necesite, pongo False en parametros
            vacio = lista.pop(0)   
    return lista

def crear_lista_dict(path:str, key:str, key2:str, key3:str, key4:str, key5:str, key6:str):
    # A. Al momento de cargar los datos desde el archivo CSV (en la opción 1 del
    # menú), el programa deberá calcular el stock disponible de cada insumo. Para
    # ello deberán crear por cada uno, un valor aleatorio entre 0 y 10. Utilizar la
    # función map.
    lista_diccionario = list(map(lambda insumo: {key:insumo[0], key2:insumo[1], key3:insumo[2], key4:float(insumo[3]), key5:insumo[4], key6:random.randint(0,10)}, leer_csv(path, True)))
    #Reccoro las lista y creo diccionarios, asignandoles keys y dejando una lista de diccionarios.
    return lista_diccionario


def mostrar_lista(lista:list):
    mensaje = 'BIENVENIDOS A LA TIENDA DE MASCOTAS'
    print(f"""{mensaje:^500s}

ID                Nombre                           Marca                  Precio                               Características                                              Stock
""")

    for item in lista:
        print(f"{item['ID']:^2s}    {item['nombre']:^32s}     {item['marca']:^25s}      ${item['precio']:.2f}     {item['caracteristicas']:<100s}   {item['stock']:<20} ")
#--------------------------------------------------------------------------------------------------------------------------------------
#2. Listar cantidad por marca:
#Muestra todas las marcas y la cantidad de insumos correspondientes a cada una.
def esta_en_lista(lista: list, item: str):
    """Verifica si la caracteristica ingresada está en la lista

    Args:
        lista (list) = Lista a ingresar
        item (str) = Caracteristica que desea verificar

    Returns:
        bool
    """
    esta_en_lista = False
    for i in lista:
        if i == item:
            esta_en_lista = True
            break
    return esta_en_lista

def contar_repetidos(lista:list, key:str, key2:str):
    """Cuenta las veces que aparece una ocurrencia en la lista ingresada

    Args:
        lista (list): Lista a ingresar
        key (str): Ocurrencia que quiera contar 
        key2 (str): key con la que aparecerá

    Returns:
        list:
    """
    lista_insumos = []
    insumos = []
    for item in lista:
        if not esta_en_lista(lista_insumos, item[key]):
            lista_insumos.append(item[key])

    for elemento in lista_insumos:
        contador = 0
        for i in lista:
            if i[key] == elemento:
                contador += 1
        insumos.append({key:elemento, key2:contador})
        
    return insumos
#--------------------------------------------------------------------------------------------------------------------------------------
#3. Listar insumos por marca: Muestra, para cada marca, el nombre y precio de los insumos correspondientes.

def listar_insumos(lista:list, key:str, key2:str, key3:str):
    """Muestra una lista de cada marca con las caracteristicas ingresadas

    Args:
        lista (list): Lista a ingresar
        key (str): Caracteristica por la que quiera listar
        key2 (str): Caracteristica que quiera agregar
        key3 (str): Caracteristica que quiera agregar

    Returns:
        list: 
    """
    lista_insumos = []
    insumos = []
    for item in lista:
        if not esta_en_lista(lista_insumos, item[key]):
            lista_insumos.append(item[key])

    for elemento in lista_insumos:
        for i in lista:
            if i[key] == elemento:
                insumos.append({key:elemento, key2:i[key2], key3:i[key3]})

    return insumos
#--------------------------------------------------------------------------------------------------------------------------------------
#4. Buscar insumo por característica: El usuario ingresa una característica (por ejemplo, "Sin Granos") y se listarán todos los
#insumos que poseen dicha característica.

def buscar_insumo(lista:list, key:str, input:str):
    """Filtra una lista por la caracteristica ingresada

    Args:
        lista (list): Lista a ingresar
        key (str): Key donde están las cosas que desea buscar
        input (str): Caracteristica ingresada por el usuario

    Returns:
        list: 
    """
    flag_estado = False
    lista_filtrada = []
    caracteristicas = input
    if caracteristicas:
        flag_estado = True

    if flag_estado:
        for item in lista:
            if re.findall(caracteristicas, item[key].lower()):
                lista_filtrada.append(item)

        if not lista_filtrada:
            print("No se encontró coincidencia.")
    else:
        print("No ha ingresado nada. Reintente")
        

    return lista_filtrada

#--------------------------------------------------------------------------------------------------------------------------------------
#5. Listar insumos ordenados: Muestra el ID, descripción, precio, marca y la primera característica de todos los productos, ordenados por
#marca de forma ascendente (A-Z) y, ante marcas iguales, por precio descendente.

def lista_ordenada(lista:list, key:str, key2:str):
    """Ordena la lista alfabéticamente de manera ascendente por el primer parametro 
    ingresado como primera opción, ante casos iguales, se ordena por el segundo parametro ingresado.

    Args:
        lista (list): Lista a ingresar
        key (str): Opcion principal a la hora de ordenar
        key2 (str): Opcion secundaria a la hora de ordenar

    Returns:
        list:
    """
    tam = len(lista)
    
    for i in range(tam - 1):
        for j in range(i + 1, tam):
            if lista[i][key] > lista[j][key]:
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux
            elif lista[i][key] == lista[j][key]:
                if float(lista[i][key2]) < float(lista[j][key2]):
                    aux = lista[i]
                    lista[i] = lista[j]
                    lista[j] = aux
    
    return lista

def primera_caracteristica(lista:list, key:str, caracter:str):
    """Busca el caracter ingresado y parte la lista, después muestra solo la primera parte

    Args:
        lista (list): Lista a ingresar
        key (str): Key de lo que quieras partir
        caracter (str): El caracter utilizado para partir la lista

    Returns:
        list: 
    """
    for item in lista:  
        item[key] = item[key].split(caracter)
        item[key] = item[key][0]

    return lista
#--------------------------------------------------------------------------------------------------------------------------------------
#6. Realizar compras: Permite realizar compras de productos. El usuario ingresa una marca y se muestran todos los productos disponibles de
#esa marca. Luego, el usuario elige un producto y la cantidad deseada. Esta acción se repite hasta que el usuario decida finalizar la compra.
#Al finalizar, se muestra el total de la compra y se genera un archivo TXT con la factura de la compra, incluyendo cantidad, producto,
#subtotal y el total de la compra.
    
def realizar_compras(lista:list, key:str, key2:str, key3:str, key4:str, key5:str, key6:str):
    # B. Realizar las modificaciones necesarias para que al momento de realizar una
# venta de productos, la misma esté condicionada por el stock disponible, si no
# hay stock disponible el programa debe informarle al usuario y sugerir que
# compre menos cantidad, en caso de que el stock sea superior a cero.
    """Permite al usuario realizar una compra. Primero muestra todos los productos de la marca ingresada, y luego el usuario
    debe agregar el producto.

    Args:
        lista (list): Lista a ingresar
        key (str): "ID"
        key2 (str): "nombre"
        key3 (str): "marca"
        key4 (str): "precio"
        key5 (str): "caracteristicas"

    Returns:
        list:
    """
    productos = []
    precio_final = 0
    while True:
        marca = input("Ingrese la marca que desee buscar: ").lower()
        marca_buscada = buscar_insumo(lista, key, marca)
        if marca_buscada:
            lista_filtrada = buscar_insumo(lista, key, marca)
            mostrar_lista(lista_filtrada)

            producto = input("Ingrese los productos deseados por ID (escriba 'volver' si deasea buscar otra marca): ")
            if producto == "volver":
                continue
            verificacion = buscar_insumo(lista_filtrada, key2, producto)
            if verificacion:
                for item in lista_filtrada:
                    if item[key2] == producto:
                        while True:
                            try:
                                cantidad = int(input("Ingrese la cantidad deseada: "))
                                if cantidad > 0:
                                    if item[key6] >= cantidad:
                                        productos.append({key3:item[key4], "Cantidad":cantidad, key5:float(item[key5])*float(cantidad)})
                                        item[key6] -= cantidad
                                        break
                                    elif item[key6] == 0:
                                        print("PRODUCTO SIN STOCK")
                                        break
                                    else:
                                        print(f"Cantidad no disponible. La cantidad de stock que hay es: {item[key6]}")
                                        continue
                                else:
                                    print("Cantidad inválida.")
                                    continue
                            except ValueError:
                                print("Cantidad inválida.")
                                continue
        
        seguir = input("¿Desea agregar otro producto a la lista? s/n: ").lower()
        while seguir != "s" and seguir != "n":
            seguir = input("¿Desea agregar otro producto a la lista? s/n: ").lower()

        if seguir == "n":
            break
      
    try: 
        if verificacion:
            for elemento in productos:
                precio_final += (elemento[key5])
                    
            crear_recibo(productos, key3, "Cantidad", key5, precio_final)
    except Exception:
        print("Compra terminada")

    return productos


def crear_recibo(producto:list, key:str, key2:str, key3:str, precio:float):
    """Recibe una lista y crea un archivo .txt

    Args:
        producto (list): Lista a ingresar
        key (str): Key que define el producto
        key2 (str): Key que define la cantidad
        key3 (str): key que define el precio
        precio (float): Resultado del precio final
    """

    with open("Recibo.txt", "w", encoding="utf8") as file:
        file.write("----RECIBO DE COMPRA---\n")
        for item in producto:
            file.write(f"Producto/s: {item[key]}\nCantidad: {item[key2]}\nPrecio: ${item[key3]:.2f}\n")
            file.write("---------------------------------------\n")
        file.write(f"PRECIO FINAL: {[precio]:.2f}")
    return file
#--------------------------------------------------------------------------------------------------------------------------------------
#7. Guardar en formato JSON: Genera un archivo JSON con todos los productos cuyo nombre contiene la palabra "Alimento".
def formato_JSON(lista:list):
    """Recibe una lista y crea un archivo .json

    Args:
        lista (list): Lista a ingresar
    """
    with open("Alimentos.json", "w", encoding="utf8") as file:
        json.dump(lista, file, indent=2,ensure_ascii=False, separators=(", ", " : "))
    
    print("GUARDADO EN FORMATO JSON EXITOSAMENTE")

    return file
#--------------------------------------------------------------------------------------------------------------------------------------
#8.Leer desde formato JSON: Permite mostrar un listado de los insumos guardados en el archivo JSON generado en la opción anterior.

def leer_json(path:str):
    """Recibe la ruta de un .json, lo guarda dentro de una variable y lo retorna.

    Args:
        path (str): Ruta a ingresar
    """
    with open (path, 'r', encoding="utf8") as file:
        insumos = json.load(file)
        
    return insumos
#--------------------------------------------------------------------------------------------------------------------------------------
#9. Actualizar precios: Aplica un aumento del 8.4% a todos los productos, utilizando la función map. Los productos actualizados se
# guardan en el archivo "Insumos.csv".

def actualizar_precios(path:str, lista:list, key:str, key2:str, key3:str, key4:str, key5:str, actualizar:float):
    """Actualiza los precios ingresados por el valor a actualizar ingresado

    Args:
        lista (list): Lista a ingresar
        key (str): "ID"
        key2 (str): "nombre"
        key3 (str): "marca"
        key4 (str): "precio"
        key5 (str): "caracteristicas"
    """
    precios_actualizados = list(map(lambda item: {key:item[key], key2:item[key2], key3:item[key3], key4:(item[key4] * actualizar / 100) + (item[key4]), key5:item[key5]}, lista))

    with open (path, 'w', encoding="utf8") as file:
        file.write("ID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS\n")
        for item in precios_actualizados:
            lista_actualizada = f"{item[key]},{item[key2]},{item[key3]},{item[key4]:.2f},{item[key5]}\n"
            file.write(lista_actualizada)
        file.write("\n")
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
 #1. El programa deberá permitir agregar un nuevo producto a la lista (mediante una nueva opción de menú).
# Al momento de ingresar la marca del producto se deberá mostrar por pantalla un
# listado con todas las marcas disponibles. Las mismas serán cargadas al programa
# desde el archivo marcas.txt.
# En cuanto a las características, se podrán agregar un mínimo de una y un máximo
# de 3.

def leer_txt(path:str):
    marcas_lista_dict = []
    with open (path, 'r', encoding="utf8") as file:
        item = file.read()
        print(item)
        marcas = item.split("\n")
        for item in marcas:
            marcas_lista_dict.append({"marca":item})
    return marcas_lista_dict    

def agregar_producto(lista:list, lista_insumos:list, key, key2, key3, key4, key5):
    flag_marca = True
    dict_producto = {}
    contador = 0
    while flag_marca:
        marca = input("Ingrese de que marca es el prodcuto: ").lower()
        if marca:
            flag_marca = False
            marca_buscada = buscar_insumo(lista, key3, marca)
            if marca_buscada:
                print("Marca encontrada")
                marca = marca_buscada[0][key3]
                dict_producto.update({key3:marca})
                while True:
                    producto = input("Ingrese el nuevo producto: ")
                    if producto:
                        dict_producto.update({key2:producto})
                        break
                    else:
                        print("Producto no ingresado.")
                        continue
                while True:
                    try:
                        precio= float(input("Ingrese un precio: "))
                    except ValueError:
                        print("precio inválido")
                        continue
                    else:
                        dict_producto.update({key4:precio})
                        break
                for ID in lista_insumos:
                    contador_ID = int(ID[key])
                    
                contador_ID += 1
                dict_producto.update({key:contador_ID})
                        
                while True:
                    caracteristica = input("Ingrese una caracterisitca: ")
                    if caracteristica:
                        dict_producto.update({key5:caracteristica})
                        break
                    else:
                        print("Caracteristica no ingresada.")
                        continue
                while True:
                    opcion = input("Desea agregar otra caracteristica? s/n: ").lower()
                    contador += 1
                    if opcion == "n":
                        break
                    elif contador == 1:
                        segunda_caracteristica = input("Ingrese la segunda carteristica: ")
                        dict_producto.update({key5:caracteristica + " | " +segunda_caracteristica})
                    elif contador == 2:
                        tercer_caracteristica = input("Ingrese la tercer carteristica: ")
                        dict_producto.update({key5:caracteristica + " | " + segunda_caracteristica + " | " + tercer_caracteristica})
                    elif contador == 3:
                        print("NO se permiten más caracterisitcas")
                        break
                    else:
                        continue
            else:
                print("Marca NO encontrada")
        else:
            print("Marca NO ingresada.")
            continue

    return dict_producto

def agregar_producto_csv_principal(producto:list, lista:list, path, key, key2, key3, key4, key5):
    lista.append(producto)
    with open (path, 'a', encoding="utf8") as file:
        file.write("\n")
        producto_nuevo = f"{producto[key]},{producto[key2]},{producto[key3]},{producto[key4]},{producto[key5]}"
        file.write(producto_nuevo)

    return lista
#--------------------------------------------------------------------------------------------------------------------------------------
# 2. Agregar una opción para guardar todos los datos actualizados (incluyendo las altas).
# El usuario elegirá el tipo de formato de exportación: csv o json.

def guardar_datos_actualizados(path:str, lista:list, key, key2, key3, key4, key5):
    productos_actualizados = list(map(lambda item: {key:str(item[key]), key2:item[key2], key3:item[key3], key4:item[key4], key5:item[key5]}, lista))
    
    if re.findall(".csv", path):
        with open (path, 'w', encoding="utf8") as file:
            file.write("ID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS\n")
            for item in productos_actualizados:
                lista_actualizada = f"{item[key]},{item[key2]},{item[key3]},{item[key4]},{item[key5]}\n"
                file.write(lista_actualizada)
        print("GUARDADO EN .CSV")

    elif re.findall(".json", path):
        with open (path, "w") as file:
            json.dump(productos_actualizados, file, indent=2,ensure_ascii=False, separators=(", ", " : "))
        print("GUARDADO EN .JSON")
    else:
        print(f"Error al crear el archivo: {path}")
    
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#Recuperatorio
# A. Al momento de cargar los datos desde el archivo CSV (en la opción 1 del
# menú), el programa deberá calcular el stock disponible de cada insumo. Para
# ello deberán crear por cada uno, un valor aleatorio entre 0 y 10. Utilizar la
# función map.

#HECHO EN LA FUNCIONA  crear_list_dict
#AGRANDAR LA CONSOLA PARA QUE SE VEA BIEN
#--------------------------------------------------------------------------------------------------------------------------------------
# B. Realizar las modificaciones necesarias para que al momento de realizar una
# venta de productos, la misma esté condicionada por el stock disponible, si no
# hay stock disponible el programa debe informarle al usuario y sugerir que
# compre menos cantidad, en caso de que el stock sea superior a cero.
#--------------------------------------------------------------------------------------------------------------------------------------
# C. Agregar opción stock por marca: Pedirle al usuario una marca y
# mostrar el stock total de los productos de esa marca.

def mostrar_stock_marca(lista:list, key:str, key2:str, key3:str, key4:str, key5:str):
    stock_total = 0
    marca = input("Ingrese la marca que desee buscar: ").lower()
    marca_buscada = buscar_insumo(lista, key3, marca)
    if marca_buscada:
        lista_filtrada = buscar_insumo(lista, key3, marca)
        mostrar_lista(lista_filtrada)

        mensaje = 'BIENVENIDOS A LA TIENDA DE MASCOTAS'
        print(f"""{mensaje:^500s}

ID                Nombre                           Marca                  Precio          Stock
        """)

        for item in lista:
            print(f"{item[key]:^2s}    {item[key2]:^32s}     {item[key3]:^25s}      ${item[key4]:.2f}           {item[key5]:<350} ")
            stock_total += item[key5]
        print(f"Stock total de los productos: {stock_total}")

#--------------------------------------------------------------------------------------------------------------------------------------
# D. Agregar opción imprimir bajo stock. Que imprima en un archivo de
# texto en formato csv. Un listado con el nombre de producto y el stock de
# aquellos productos que tengan 2 o menos unidades de stock.

def imprimir_bajo_stock(lista:list, path, key, key2):
    lista_stock_bajo = []
    for item in lista:
        if item[key2] <= 2:
            lista_stock_bajo.append({key:item[key], key2:item[key2]})

    with open (path, 'w', encoding="utf8") as file:
            file.write("MARCA,STOCK\n")
            for item in lista_stock_bajo:
                lista_actualizada = f"{item[key]},{item[key2]}\n"
                file.write(lista_actualizada)
    
    print("GUARDADO EN .CSV")




    















#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------
#*************************************************FUNCIONES MENU***********************************************************************

def menu():
    os.system("cls")
    print("""***Bienvenidos a la Tienda de Mascotas***
    1-Cargar datos
    2-Listar cantidad por marca
    3-Listar insumos por marca
    4-Buscar insumo por característica
    5-Listar insumos ordenados con una sola característica
    6-Realizar compras
    7-Guardar Alimentos en formato JSON
    8-Leer formato JSON
    9-Actualizar precios
    10-Agregar nuevo producto a la lista
    11-Guardar la lista de insumos en .csv o .json
    12-Mostrar stock de marca
    13-Imprimir bajo stock
    12-Salir
    """)
    while True:
        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("Eso NO es un número")
        else:
            return opcion

def elegir_opcion(opcion):
    path = "insumos.csv"
    lista_insumos = crear_lista_dict(path, "ID", "nombre", "marca", "precio", "caracteristicas", "stock")
    match opcion:
        case 1:
            mostrar_lista((crear_lista_dict(path, "ID", "nombre", "marca", "precio", "caracteristicas", "stock")))
        case 2:
            lista_contada = contar_repetidos(lista_insumos, "marca", "cantidad")
            for item in lista_contada:
                print(f"Marca: {item['marca']}\nCantidad: {item['cantidad']}")
                print("-------------------------")
        case 3:
            insumos_listados = listar_insumos(lista_insumos, "marca", "nombre", "precio")
            for item in insumos_listados:
                print(f"Marca: {item['marca']}\nNombre: {item['nombre']}\nPrecio: {item['precio']}")
                print("-------------------------")
        case 4:
            caracteristicas = input("Ingrese la caracteristicas que desee buscar: ").lower()
            insumo_buscado = buscar_insumo(lista_insumos, "caracteristicas", caracteristicas)
            if insumo_buscado:
                mostrar_lista(insumo_buscado)
        case 5:
            insumos_ordenados = lista_ordenada(lista_insumos, "marca", "precio")
            insumos_ordenados = primera_caracteristica(insumos_ordenados, "caracteristicas", " | ")
            mostrar_lista(insumos_ordenados)
        case 6:
            realizar_compras(lista_insumos,"marca", "ID", "Producto", "nombre", "precio", "stock")
        case 7:
            lista_especifica = buscar_insumo(lista_insumos, "nombre", "alimento")
            return formato_JSON(lista_especifica)
        case 8:
            path = "Alimentos.json"
            insumos = leer_json(path)
            mostrar_lista(insumos)
        case 9:
            lista_actualizada = actualizar_precios(path, lista_insumos, "ID", "nombre", "marca", "precio", "caracteristicas", 8.4)
            return lista_actualizada
        case 10: 
            path_txt = "marcas.txt"
            marcas = leer_txt(path_txt)
            while True:
                producto_nuevo = agregar_producto(marcas, lista_insumos, "ID", "nombre", "marca", "precio", "caracteristicas")
                if producto_nuevo:
                    agregar_producto_csv_principal(producto_nuevo, lista_insumos, path, "ID", "nombre", "marca", "precio", "caracteristicas")

                seguir = input("Desea agregar otro producto? s/n: ").lower()
                if seguir == "s":
                    continue
                else:
                    break
        case 11:
            while True:
                guardar = input("guardar en .csv o .json: ").lower()
                if guardar == ".csv":
                    guardar_datos_actualizados("insumos_nuevos.csv", lista_insumos, "ID", "nombre", "marca", "precio", "caracteristicas")
                    break
                elif guardar == ".json":
                    guardar_datos_actualizados("insumos_nuevos.json", lista_insumos, "ID", "nombre", "marca", "precio", "caracteristicas")
                    break
                else:
                    print("Tipo de archivo inválido. Reintente")
                    continue
        case 12:
            mostrar_stock_marca(lista_insumos, "ID", "nombre", "marca", "precio", "stock")
        case 13:
            imprimir_bajo_stock(lista_insumos, "Productos con bajo stock.csv" ,"nombre","stock")
        case 14:
            salir = input("Seguro que desea salir? s/n: ").lower()
            return salir 
        case _:
            print("ERROR. Opción inválida")