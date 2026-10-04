# SECURELINK - Implementación educativa de RC4
def ksa(clave):
    """
    Key Scheduling Algorithm (KSA).
    Genera el estado inicial de RC4.
    """

    S = list(range(256))
    j = 0

    clave_bytes = clave.encode("utf-8")

    for i in range(256):
        j = (j + S[i] + clave_bytes[i % len(clave_bytes)]) % 256

        S[i], S[j] = S[j], S[i]

    return S


def prga(S):
    """
    Pseudo-Random Generation Algorithm (PRGA).
    Genera el flujo de claves de RC4.
    """

    i = 0
    j = 0

    while True:

        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]

        K = S[(S[i] + S[j]) % 256]

        yield K


def rc4(mensaje, clave):
    """
    Cifra o descifra un mensaje utilizando RC4.

    RC4 utiliza XOR, por lo que la misma función
    permite cifrar y descifrar.
    """

    S = ksa(clave)
    generador = prga(S)

    resultado = bytearray()

    for byte in mensaje:
        resultado.append(byte ^ next(generador))

    return bytes(resultado)


def main():

    print("==========================================")
    print(" SECURELINK - TOKEN CON RC4")
    print("==========================================")
    print()

    # Generación del mensaje/token

    token = "SECURELINK-2026-USER-001"

    clave = "CLAVE_SECURELINK"

    print("Token original:")
    print(token)

    print()
    print("Clave utilizada:")
    print(clave)

    # Cifrado

    token_cifrado = rc4(
        token.encode("utf-8"),
        clave
    )

    print()
    print("Token cifrado en hexadecimal:")
    print(token_cifrado.hex())

    # Descifrado

    token_descifrado = rc4(
        token_cifrado,
        clave
    )

    print()
    print("Token descifrado:")
    print(token_descifrado.decode("utf-8"))

    # Comprobación

    print()

    if token == token_descifrado.decode("utf-8"):

        print("✓ PRUEBA EXITOSA")
        print("El token original y el descifrado coinciden.")

    else:

        print("✗ ERROR")
        print("Los tokens no coinciden.")


if __name__ == "__main__":
    main()