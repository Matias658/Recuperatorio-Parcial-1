from funciones import *
import os
flag_cargar_datos = False
flag_leer_json = False
flag_precios_actualizados = False
flag_json_creado = False


while True:
    os.system("cls")
    opcion = menu()
    if opcion == 1:
        flag_cargar_datos = True
        mensaje = 'Datos cargados con exito'
        print(f"{mensaje:^500s}")
    elif flag_cargar_datos or opcion == 14:
        match opcion:
            case 7:
                flag_leer_json = True
                if flag_json_creado:
                    print("Ya se creó el archivo .json anteriormente.")
                    os.system("pause")
                    continue
                flag_json_creado = True

            case 8:
                if flag_leer_json == False:
                    print("PRIMERO LEA EL JSON")
                    os.system("pause")
                    continue
                else:
                    pass
            case 9:
                if flag_precios_actualizados:
                    print("Ya se actualizó la lista anteriormente.")
                    os.system("pause")
                    continue
                flag_precios_actualizados = True

                
                
    else:
        print("PRIMERO CARGUE LOS DATOS POR FAVOR")
        os.system("pause")
        continue


    salir = elegir_opcion(opcion)
    if salir == "s":
        break
    os.system("pause")
# 1. Alumnos que hayan obtenido un 4 y deseen levantar nota: deberán
# presentar el mismo trabajo que en la instancia anterior con las modificaciones
# que marcamos en las devoluciones.
# A. Al momento de cargar los datos desde el archivo CSV (en la opción 1 del
# menú), el programa deberá calcular el stock disponible de cada insumo. Para
# ello deberán crear por cada uno, un valor aleatorio entre 0 y 10. Utilizar la
# función map.
# B. Realizar las modificaciones necesarias para que al momento de realizar una
# venta de productos, la misma esté condicionada por el stock disponible, si no
# hay stock disponible el programa debe informarle al usuario y sugerir que
# compre menos cantidad, en caso de que el stock sea superior a cero.

# 2. Alumnos que aún no hayan aprobado el parcial: deberán presentar lo
# mismo que para el caso de los alumnos que se presenta para levantar nota
# (Puntos A y B ) y además deberán agregar lo siguiente:

# C. Agregar opción stock por marca: Pedirle al usuario una marca y
# mostrar el stock total de los productos de esa marca.
# D. Agregar opción imprimir bajo stock. Que imprima en un archivo de
# texto en formato csv. Un listado con el nombre de producto y el stock de
# aquellos productos que tengan 2 o menos unidades de stock.