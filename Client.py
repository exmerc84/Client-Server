import asyncio
import ssl

async def main():
    username = 'usuario1'
    password = 'contraseña1'
    credenciales = f"{username},{password}"

    # Parámetros a enviar (10 parámetros diferentes)
    parametros = [
        "valor1", "valor2", "valor3", "valor4", "valor5",
        "valor6", "valor7", "valor8", "valor9", "valor10"
    ]
    mensaje_parametros = ','.join(parametros)

    # Configuración SSL del cliente
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='cert.pem')
    ssl_context.check_hostname = False  # Desactiva la verificación del nombre de host

    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, ssl=ssl_context)

    # Enviar credenciales
    writer.write((credenciales + '\n').encode())
    await writer.drain()

    # Enviar parámetros
    writer.write((mensaje_parametros + '\n').encode())
    await writer.drain()

    # Leer respuesta del servidor
    data = await reader.readline()
    respuesta = data.decode().strip()
    print(f"Respuesta del servidor: {respuesta}")

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
