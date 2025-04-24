import mysql.connector
import getpass
import os

conexion = None

def limpiarPantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def conectarBasedatos():
    global conexion
    usuario = input("Introduce el usuario: ")
    password = getpass.getpass("Introduce la password: ")
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user=usuario,
            password=password,
            database="classicmodels"
        )
        print("\nConectado")
    except mysql.connector.Error as err:
        print("Error")
        conexion = None

def mostrar_directivos():
    if not conexion:
        print("Error -> Se ha perdido la conexion")
        return
    # Realizamos la consulta seleccionando las columnas que se nos piden y las renombramos
    # Incluimos employeeNumber al principio
    query = """
        SELECT employeeNumber AS ID, lastName AS Apellido, firstName AS Nombre, email AS Email, jobTitle AS Puesto
        FROM employees
        WHERE jobTitle LIKE '%VP%' OR jobTitle LIKE '%Director%'
        ORDER BY lastName, firstName
    """
    try:
        # Creamos un cursor para ejecutar la consulta
        cursor = conexion.cursor()
        cursor.execute(query)
        # Mostramos los resultados de forma legible
        print(f"\n{'ID':6} {'Apellido':20} {'Nombre':20} {'Email':30} {'Puesto'}")
        print("-" * 90)
        for fila in cursor.fetchall():
            print(f"{fila[0]:6} {fila[1]:20} {fila[2]:20} {fila[3]:30} {fila[4]}")
        cursor.close()
    except mysql.connector.Error as err:
        print("Error -> Se ha perdido la conexion")

def mostrar_top_clientes():
    if not conexion:
        print("Error -> Se ha perdido la conexion")
        return

    query = """
        SELECT c.customerNumber AS ID,
               c.customerName AS Nombre,
               SUM(p.amount) AS Total_Pagos
        FROM customers c
        JOIN payments p ON c.customerNumber = p.customerNumber
        GROUP BY c.customerNumber, c.customerName
        ORDER BY Total_Pagos DESC
        LIMIT 10
    """
    try:
        cursor = conexion.cursor()
        cursor.execute(query)
        print(f"\n{'ID':6} {'Nombre':35} {'Total_Pagos'}")
        print("-" * 60)
        for fila in cursor.fetchall():
            print(f"{fila[0]:6} {fila[1]:35} {fila[2]:.2f}")
        cursor.close()
    except mysql.connector.Error as err:
        print("Error")

def menu_principal():
    while True:
        print("/*/*/*/*/*  MENU PRINCIPAL  */*/*/*/*/")
        print("0 -> Borrar pantalla")
        print("1 -> Introducir usuario y password")
        print("2 -> Mostrar el Listado de Directivos de la empresa classicmodels")
        print("3 -> Mostrar el Top 10 de Clientes")
        print("4 -> Salir")
        opcion = input("Elige una opción: ")

        match opcion:
            case "0":
                limpiarPantalla()
            case "1":
                conectarBasedatos()
            case "2":
                mostrar_directivos()
            case "3":
                mostrar_top_clientes()
            case "4":
                print("Has salido")
                if conexion:
                    conexion.close()
                break
            case _:
                print("Input incorrecto -> prueba otra vez")

if __name__ == "__main__":
    menu_principal()
