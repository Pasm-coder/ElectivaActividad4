# SECURELINK - Simulación educativa de RC5

def rotl(value, shift, bits=32):
    """Rotación circular hacia la izquierda."""
    shift %= bits
    mask = (1 << bits) - 1
    return ((value << shift) | (value >> (bits - shift))) & mask


def rotr(value, shift, bits=32):
    """Rotación circular hacia la derecha."""
    shift %= bits
    mask = (1 << bits) - 1
    return ((value >> shift) | (value << (bits - shift))) & mask


def cifrar_bloque(bloque, clave):
    """
    Simulación simplificada de operaciones similares
    a las utilizadas en RC5: XOR, suma modular y rotaciones.
    """

    bits = 32
    mask = (1 << bits) - 1

    A = int.from_bytes(bloque[:4].ljust(4, b'\x00'), 'big')
    B = int.from_bytes(bloque[4:8].ljust(4, b'\x00'), 'big')

    K = int.from_bytes(clave[:4].ljust(4, b'\x00'), 'big')

    for i in range(4):
        A = (A + K) & mask
        A ^= B
        A = rotl(A, B % bits, bits)

        B = (B + K) & mask
        B ^= A
        B = rotl(B, A % bits, bits)

    return A.to_bytes(4, 'big') + B.to_bytes(4, 'big')


def descifrar_bloque(bloque, clave):
    """Revierte las operaciones de la simulación."""

    bits = 32
    mask = (1 << bits) - 1

    A = int.from_bytes(bloque[:4], 'big')
    B = int.from_bytes(bloque[4:8], 'big')

    K = int.from_bytes(clave[:4].ljust(4, b'\x00'), 'big')

    for i in range(3, -1, -1):

        B = rotr(B, A % bits, bits)
        B ^= A
        B = (B - K) & mask

        A = rotr(A, B % bits, bits)
        A ^= B
        A = (A - K) & mask

    return A.to_bytes(4, 'big') + B.to_bytes(4, 'big')


def main():

    archivo_original = "archivo_original.txt"
    archivo_cifrado = "archivo_cifrado_rc5.bin"
    archivo_descifrado = "archivo_descifrado_rc5.txt"

    clave = b"CLAVE123"

    # Leer archivo original

    with open(archivo_original, "rb") as archivo:
        datos = archivo.read()

    print("=== SIMULACIÓN RC5 - SECURELINK ===")
    print()
    print("Archivo original:")
    print(datos.decode("utf-8"))

    # Cifrado

    datos_cifrados = b""

    for i in range(0, len(datos), 8):
        bloque = datos[i:i + 8]
        datos_cifrados += cifrar_bloque(bloque, clave)

    with open(archivo_cifrado, "wb") as archivo:
        archivo.write(datos_cifrados)

    print()
    print("Archivo cifrado generado:")
    print(archivo_cifrado)

    print()
    print("Contenido cifrado en hexadecimal:")
    print(datos_cifrados.hex())

    # Descifrado

    datos_descifrados = b""

    for i in range(0, len(datos_cifrados), 8):
        bloque = datos_cifrados[i:i + 8]
        datos_descifrados += descifrar_bloque(bloque, clave)

    datos_descifrados = datos_descifrados.rstrip(b"\x00")

    with open(archivo_descifrado, "wb") as archivo:
        archivo.write(datos_descifrados)

    print()
    print("Archivo descifrado generado:")
    print(archivo_descifrado)

    print()
    print("Contenido descifrado:")
    print(datos_descifrados.decode("utf-8"))

    print()
    if datos == datos_descifrados:
        print("✓ PRUEBA EXITOSA: el contenido original y el descifrado coinciden.")
    else:
        print("✗ ERROR: los contenidos no coinciden.")


if __name__ == "__main__":
    main()