# SECURELINK - Firma digital y verificación con RSA

import hashlib
import secrets


# Funciones matemáticas auxiliares

def es_primo(n):
    if n < 2:
        return False

    if n % 2 == 0:
        return n == 2

    divisor = 3

    while divisor * divisor <= n:
        if n % divisor == 0:
            return False

        divisor += 2

    return True


def generar_primo():
    while True:
        numero = secrets.randbelow(200) + 100

        if es_primo(numero):
            return numero


def mcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a


def inverso_modular(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x

    raise ValueError("No existe inverso modular")


# Generación de claves RSA

def generar_claves():

    p = generar_primo()
    q = generar_primo()

    while p == q:
        q = generar_primo()

    n = p * q

    phi = (p - 1) * (q - 1)

    e = 65537

    # En caso de que el valor elegido no sea válido
    if mcd(e, phi) != 1:

        e = 3

        while mcd(e, phi) != 1:
            e += 2

    d = inverso_modular(e, phi)

    clave_publica = (e, n)
    clave_privada = (d, n)

    return clave_publica, clave_privada


# Hash SHA-256

def obtener_hash(mensaje):

    return int.from_bytes(
        hashlib.sha256(mensaje).digest(),
        "big"
    )


# Firma digital

def firmar(mensaje, clave_privada):

    d, n = clave_privada

    hash_mensaje = obtener_hash(mensaje)

    firma = pow(hash_mensaje, d, n)

    return firma


# Verificación

def verificar(mensaje, firma, clave_publica):

    e, n = clave_publica

    hash_original = obtener_hash(mensaje)

    hash_firma = pow(firma, e, n)

    return hash_original % n == hash_firma


# Programa principal

def main():

    print("==========================================")
    print(" SECURELINK - FIRMA DIGITAL RSA")
    print("==========================================")
    print()

    # Generar claves
    clave_publica, clave_privada = generar_claves()

    print("Clave pública:")
    print(clave_publica)

    print()

    print("Clave privada:")
    print(clave_privada)

    print()

    # Mensaje
    mensaje = input(
        "Ingrese el mensaje que desea firmar: "
    ).encode("utf-8")

    # Crear firma
    firma = firmar(
        mensaje,
        clave_privada
    )

    print()
    print("Firma digital generada:")
    print(firma)

    # Verificación
    resultado = verificar(
        mensaje,
        firma,
        clave_publica
    )

    print()

    if resultado:
        print("✓ FIRMA VÁLIDA")
        print("La firma coincide con el mensaje.")
    else:
        print("✗ FIRMA INVÁLIDA")

    # Prueba de modificación del mensaje

    mensaje_modificado = (
        mensaje + b" MODIFICADO"
    )

    resultado_modificado = verificar(
        mensaje_modificado,
        firma,
        clave_publica
    )

    print()
    print("Prueba modificando el mensaje:")

    if resultado_modificado:
        print("✗ ERROR: la modificación no fue detectada.")
    else:
        print("✓ MODIFICACIÓN DETECTADA")
        print("La firma ya no coincide con el mensaje.")


if __name__ == "__main__":
    main()