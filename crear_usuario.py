import bcrypt
import mysql.connector
import getpass


usuario = input("Ingrese el nombre de usuario: ").strip()

password = getpass.getpass("Ingrese la contraseña: ")

print("\nSeleccione el rol:")
print("1. admin")
print("2. usuario")
print("3. invitado")

opcion = input("Opción: ").strip()

roles = {
    "1": "admin",
    "2": "usuario",
    "3": "invitado"
}

rol = roles.get(opcion)

if not rol:
    print("Rol no válido.")
    exit()


conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securelink"
)

cursor = conexion.cursor()


cursor.execute(
    "SELECT id FROM usuarios WHERE usuario = %s",
    (usuario,)
)

if cursor.fetchone():
    print("Ese usuario ya existe.")
    cursor.close()
    conexion.close()
    exit()


password_hash = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")


sql = """
INSERT INTO usuarios (usuario, password_hash, rol)
VALUES (%s, %s, %s)
"""

cursor.execute(
    sql,
    (usuario, password_hash, rol)
)

conexion.commit()

print("\nUsuario creado correctamente.")
print(f"Usuario: {usuario}")
print(f"Rol: {rol}")


cursor.close()
conexion.close()