import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="securelink"
)

if conexion.is_connected():
    print("Conexión exitosa con MySQL/MariaDB.")

conexion.close()