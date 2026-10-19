import sqlite3
import os

# CONFIGURACIÓN DE LA BASE DE DATOS
DB = "database/alumnos.db"


def conectar():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DB)

# CREACIÓN DE LA BASE DE DATOS

def crear_bd():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            curp TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            calle TEXT,
            colonia TEXT,
            telefono TEXT,
            edad TEXT
            sueldo_mensual TEXT
        )
    """)

    conexion.commit()
    conexion.close()

# 1. ALTAS DE EMPLEADOS

def alta_empleados():
    print("\n===== ALTA DE EMPLEADOS =====")

    curp = input("Curp: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    telefono = input("Teléfono: ").strip()
    edad = input("Edad: ").strip()
    sueldo_mensual = input("Sueldo Mensual: ").strip()

    if not curp or not nombre or not apellido:
        print("La CURP, el nombre y el apellido son obligatorios.")
        return

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO alumno (
                curp, nombre, apellido, calle,
                colonia, telefono, edad, sueldo_mensual
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            curp, nombre, apellido, calle,
            colonia, telefono, edad, sueldo_mensual
        ))

        conexion.commit()
        print("\nEmpleado registrado correctamente.")

    except sqlite3.IntegrityError:
        print("\nError: la curp ya existe.")

    except sqlite3.Error as error:
        print("Error al registrar al empleado:", error)

    finally:
        conexion.close()


# 2. BAJAS DE EMPLEADOS

def baja_empleados():
    print("\n===== BAJA DE EMPLEADOS =====")

    curp = input("curp del empleado: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM empleados
            WHERE curp = ?
        """, (curp,))

        empleados = cursor.fetchone()

        if empleados is None:
            print("No se encontró un empleados con esa curp.")
            return

        print("\nDatos del empleado:")
        print("Matrícula:", empleados[0])
        print("Nombre:", empleados[1])
        print("Apellido:", empleados[2])
        print("Calle:", empleados[3])
        print("Colonia:", empleados[4])
        print("Teléfono:", empleados[5])
        print("Edad:", empleados[6])
        print("sueldo_mensual", empleados [7])

        confirmacion = input(
            "\n¿Desea eliminar este empleado? (S/N): "
        ).strip().upper()

        if confirmacion == "S":
            cursor.execute("""
                DELETE FROM empleados
                WHERE curp = ?
            """, (curp,))

            conexion.commit()
            print("Empleado eliminado correctamente.")
        else:
            print("Operación cancelada.")

    except sqlite3.Error as error:
        print("Error al eliminar al empleado:", error)

    finally:
        conexion.close()


# 3. MODIFICACIONES DE EMPLEADOS

def modificar_empleado():
    print("\n===== MODIFICACIÓN DE EMPLEADO =====")

    curp = input("curp del empleado: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT nombre, apellido, calle, colonia,
                   telefono, edad, sueldo_mensual
            FROM empleado
            WHERE curp = ?
        """, (curp,))

        empleado = cursor.fetchone()

        if empleado is None:
            print("No se encontró un empleado con esa curp. ")
            return

        print("\nIngrese los nuevos datos.")
        print("Presione ENTER para conservar el dato actual.")

        nombre = input(f"Nombre [{empleado[0]}]: ").strip()
        apellido = input(f"Apellido [{empleado[1]}]: ").strip()
        calle = input(f"Calle [{empleado[2] or ''}]: ").strip()
        colonia = input(f"Colonia [{empleado[3] or ''}]: ").strip()
        telefono = input( f"telefono [{empleado[4] or ''}]: ").strip()
        edad = input(f"Edad [{empleado[5] or ''}]: ").strip()
        sueldo_mensual = input(f"sueldo_mensual [{empleado [6] or ''}]: ").strip ()

        # Conservar los valores anteriores cuando se pulsa ENTER
        nombre = nombre or empleado[0]
        apellido = apellido or empleado[1]
        calle = calle or empleado[2] or ""
        colonia = colonia or empleado[3] or ""
        telefono = telefono or empleado[4] or ""
        edad = edad or empleado[5] or ""
        sueldo_mensual = sueldo_mensual or empleado [6] or ""

        cursor.execute("""
            UPDATE empleado
            SET nombre = ?,
                apellido = ?,
                calle = ?,
                colonia = ?,
                telefono = ?,
                edad = ?,
                sueldo_mensual = ?
            WHERE curp = ?
        """, (
            nombre, apellido, calle, colonia,
            telefono, edad, sueldo_mensual, curp
        ))

        conexion.commit()
        print("\nEmpleado modificado correctamente.")

    except sqlite3.Error as error:
        conexion.rollback()
        print("Error al modificar al empleado:", error)

    finally:
        conexion.close()

# 4. CONSULTA DE TODA LA TABLA

def consultar_todos():
    print("\n===== LISTADO DE EMPLEADOS =====")

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT matricula, nombre, apellido, calle,
                   colonia, telefono , edad, sueldo_mensual
            FROM empleados
            ORDER BY apellido, nombre
        """)

        empleados = cursor.fetchall()

        if not empleados:
            print("No hay empleados registrados.")
            return

        for empleado in empleados:
            print("-" * 50)
            print("Matrícula:", empleado[0])
            print("Nombre:", empleado[1])
            print("Apellido:", empleado[2])
            print("Calle:", empleado[3] or "")
            print("Colonia:", empleado[4] or "")
            print("Telefono:", empleado[5] or "")
            print("Edad:", empleado[6] or "")
            print("Sueldo_mensual"[7] or "")

        print("-" * 50)
        print("Total de empleados:", len(empleados))

    except sqlite3.Error as error:
        print("Error al consultar los empleados:", error)

    finally:
        conexion.close()

# 5. CONSULTA POR CURP

def consultar_curp ():
    print("\n===== CONSULTA POR CURP =====")

    curp = input("Ingrese la curp: ").strip()

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT curp, nombre, apellido, calle,
                   colonia, telefono , edad, sueldo_mensual
            FROM empleados
            WHERE curp = ?
        """, (curp,))

        empleados = cursor.fetchone()

        if empleados :
            print("\n===== DATOS DEL ALUMNO =====")
            print("Matrícula:", empleados[0])
            print("Nombre:", empleados[1])
            print("Apellido:", empleados[2])
            print("Calle:", empleados[3] or "")
            print("Colonia:", empleados[4] or "")
            print("Teléfono:", empleados[5] or "")
            print("Edad:", empleados[6] or "")
            print("Sueldo mensual:", empleados[7] or "")
        else:
            print("No se encontró un empleado con esa curp.")

    except sqlite3.Error as error:
        print("Error al consultar al empleado:", error)

    finally:
        conexion.close()

# 6. MENÚ PRINCIPAL
def menu():
    while True:
        print("\n" + "=" * 45)
        print("       SISTEMA DE CONTROL DE EMPLEADOS")
        print("=" * 45)
        print("1. Alta de empleados")
        print("2. Baja de empleados")
        print("3. Modificación de empleados")
        print("4. Consulta de toda la tabla")
        print("5. Consulta por curp")
        print("6. Salir del sistema")
        print("=" * 45)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            alta_empleados()

        elif opcion == "2":
            baja_empleados()

        elif opcion == "3":
            modificar_empleado()

        elif opcion == "4":
            consultar_todos()

        elif opcion == "5":
            consultar_curp()

        elif opcion == "6":
            print("\nSaliendo del sistema...")
            print("Gracias por utilizar el sistema.")
            break

        else:
            print("\nOpción inválida. Seleccione del 1 al 6.")