from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import mysql.connector


app = Flask(__name__)


app.secret_key = "SECURELINK_CLAVE_SECRETA_2026"


# CONEXIÓN CON MYSQL / MARIADB

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="securelink"
    )


# CREAR USUARIOS INICIALES

def crear_usuarios_iniciales():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    usuarios = [
        ("admin1", "Admin123!", "admin"),
        ("usuario1", "Usuario123!", "usuario"),
        ("invitado1", "Invitado123!", "invitado")
    ]

    for usuario, password, rol in usuarios:

        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (usuario,)
        )

        existe = cursor.fetchone()

        if not existe:

            password_hash = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            cursor.execute(
                """
                INSERT INTO usuarios
                (usuario, password_hash, rol)
                VALUES (%s, %s, %s)
                """,
                (usuario, password_hash, rol)
            )

    conexion.commit()

    cursor.close()
    conexion.close()


# INICIO

@app.route("/")
def inicio():

    return redirect(url_for("login"))


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    mensaje = ""

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT usuario, password_hash, rol
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario,)
        )

        usuario_db = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario_db:

            password_correcta = bcrypt.checkpw(
                password.encode("utf-8"),
                usuario_db["password_hash"].encode("utf-8")
            )

            if password_correcta:

                session["usuario"] = usuario_db["usuario"]
                session["rol"] = usuario_db["rol"]

                rol = usuario_db["rol"]

                if rol == "admin":
                    return redirect(url_for("admin"))

                elif rol == "usuario":
                    return redirect(url_for("user"))

                elif rol == "invitado":
                    return redirect(url_for("guest"))

        mensaje = "Usuario o contraseña incorrectos."

    return render_template(
        "login.html",
        mensaje=mensaje
    )


# REGISTRO DE USUARIOS

@app.route("/registro", methods=["GET", "POST"])
def registro():

    mensaje = ""

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        
        if not usuario or not password:
            mensaje = "Todos los campos son obligatorios."
            return render_template(
                "registro.html",
                mensaje=mensaje
            )

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        
        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (usuario,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conexion.close()

            mensaje = "El usuario ya existe."

            return render_template(
                "registro.html",
                mensaje=mensaje
            )

        
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        
        cursor.execute(
            """
            INSERT INTO usuarios
            (usuario, password_hash, rol)
            VALUES (%s, %s, %s)
            """,
            (usuario, password_hash, "usuario")
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        mensaje=mensaje
    )



# RUTA ADMIN

@app.route("/admin")
def admin():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("rol") != "admin":
        return redirect(url_for("login"))

    return render_template(
        "admin.html",
        usuario=session["usuario"]
    )


# RUTA USUARIO

@app.route("/user")
def user():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("rol") != "usuario":
        return redirect(url_for("login"))

    return render_template(
        "user.html",
        usuario=session["usuario"]
    )


# RUTA INVITADO

@app.route("/guest")
def guest():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if session.get("rol") != "invitado":
        return redirect(url_for("login"))

    return render_template(
        "guest.html",
        usuario=session["usuario"]
    )


# CERRAR SESIÓN

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# EJECUCIÓN

if __name__ == "__main__":

    crear_usuarios_iniciales()

    app.run(
        debug=True
    )