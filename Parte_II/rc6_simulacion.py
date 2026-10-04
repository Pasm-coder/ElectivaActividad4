# SECURELINK - Simulación educativa de RC6

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
    Simulación simplificada del funcionamiento de RC6
    utilizando suma modular, XOR y rotaciones.
    """

    bits = 32
    mask = (1 << bits) - 1

    # RC6 trabaja conceptualmente con cuatro registros.
    A = int.from_bytes(bloque[0:4].ljust(4, b'\x00'), 'big')
    B = int.from_bytes(bloque[4:8].ljust(4, b'\x00'), 'big')
    C = int.from_bytes(bloque[8:12].ljust(4, b'\x00'), 'big')
    D = int.from_bytes(bloque[12:16].ljust(4, b'\x00'), 'big')

    K = int.from_bytes(clave[:4].ljust(4, b'\x00'), 'big')

    # Simulación de rondas.
    for ronda in range(4):

        B = (B + K) & mask
        D = (D + K) & mask

        t = rotl(
            (B * ((2 * B + 1) & mask)) & mask,
            5,
            bits
        )

        u = rotl(
            (D * ((2 * D + 1) & mask)) & mask,
            5,
            bits
        )

        A ^= t
        C ^= u

        A = rotl(A, u % bits, bits)
        C = rotl(C, t % bits, bits)

        # Rotación de registros
        A, B, C, D = B, C, D, A

    return (
        A.to_bytes(4, 'big') +
        B.to_bytes(4, 'big') +
        C.to_bytes(4, 'big') +
        D.to_bytes(4, 'big')
    )


def descifrar_bloque(bloque, clave):
    """
    Para esta actividad se realiza una simulación reversible
    utilizando XOR y operaciones básicas.
    """

    bits = 32
    mask = (1 << bits) - 1

    A = int.from_bytes(bloque[0:4], 'big')
    B = int.from_bytes(bloque[4:8], 'big')
    C = int.from_bytes(bloque[8:12], 'big')
    D = int.from_bytes(bloque[12:16], 'big')

    K = int.from_bytes(clave[:4].ljust(4, b'\x00'), 'big')

    # Revertimos las rondas.
    for ronda in range(3, -1, -1):

        # Revertir rotación de registros
        A, B, C, D = D, A, B, C

        t = rotl(
            (B * ((2 * B + 1) & mask)) & mask,
            5,
            bits
        )

        u = rotl(
            (D * ((2 * D + 1) & mask)) & mask,
            5,
            bits
        )

        A = rotr(A, u % bits, bits)
        C = rotr(C, t % bits, bits)

        A ^= t
        C ^= u

        B = (B - K) & mask
        D = (D - K) & mask

    return (
        A.to_bytes(4, 'big') +
        B.to_bytes(4, 'big') +
        C.to_bytes(4, 'big') +
        D.to_bytes(4, 'big')
    )


def main():

    archivo_original = "archivo_original.txt"
    archivo_cifrado = "archivo_cifrado_rc6.bin"
    archivo_descifrado = "archivo_descifrado_rc6.txt"

    clave = b"CLAVE123"

    # Leer archivo original

    with open(archivo_original, "rb") as archivo:
        datos = archivo.read()

    print("=== SIMULACIÓN RC6 - SECURELINK ===")
    print()
    print("Archivo original:")
    print(datos.decode("utf-8"))

    # Cifrado

    datos_cifrados = b""

    for i in range(0, len(datos), 16):
        bloque = datos[i:i + 16]
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

    for i in range(0, len(datos_cifrados), 16):
        bloque = datos_cifrados[i:i + 16]
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