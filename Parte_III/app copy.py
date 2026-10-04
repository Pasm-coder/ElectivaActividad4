from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import json
import os


app = Flask(__name__)

app.secret_key = "SECURELINK_CLAVE_SECRETA_2026"


ARCHIVO_USUARIOS = "usuarios.json"


# FUNCIONES PARA MANEJAR USUARIOS

def cargar_usuarios():

    if not os.path.exists(ARCHIVO_USUARIOS):
        return {}

    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_usuarios(usuarios):

    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
        json.dump(
            usuarios,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def crear_usuarios_iniciales():

    usuarios = cargar_usuarios()

    if usuarios:
        return

    usuarios = {
        "admin1": {
            "password": bcrypt.hashpw(
                b"Admin123!",
                bcrypt.gensalt()
            ).decode("utf-8"),
            "rol": "admin"
        },

        "usuario1": {
            "password": bcrypt.hashpw(
                b"Usuario123!",
                bcrypt.gensalt()
            ).decode("utf-8"),
            "rol": "usuario"
        },

        "invitado1": {
            "password": bcrypt.hashpw(
                b"Invitado123!",
                bcrypt.gensalt()
            ).decode("utf-8"),
            "rol": "invitado"
        }
    }

    guardar_usuarios(usuarios)


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

        usuarios = cargar_usuarios()

        if usuario in usuarios:

            password_hash = usuarios[usuario]["password"]

            password_correcta = bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8")
            )

            if password_correcta:

                session["usuario"] = usuario
                session["rol"] = usuarios[usuario]["rol"]

                rol = usuarios[usuario]["rol"]

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