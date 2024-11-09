import asyncio
import ssl

# Diccionario de usuarios autorizados
usuarios_autorizados = {
    'usuario1': 'contraseña1',
    'usuario2': 'contraseña2',
    # Agrega más usuarios y contraseñas según sea necesario
}

async def manejar_cliente(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conexión desde {addr}")

    try:
        # Paso 1: Autenticación
        data = await reader.readline()
        credenciales = data.decode().strip().split(',')
        if len(credenciales) != 2:
            respuesta = "Error: formato de autenticación inválido."
            writer.write(respuesta.encode() + b'\n')
            await writer.drain()
            return

        username, password = credenciales
        if usuarios_autorizados.get(username) != password:
            respuesta = "Error: autenticación fallida."
            writer.write(respuesta.encode() + b'\n')
            await writer.drain()
            return

        print(f"Usuario {username} autenticado exitosamente.")

        # Paso 2: Recepción de 10 parámetros
        data = await reader.readline()
        parametros = data.decode().strip().split(',')
        if len(parametros) == 10:
            # Almacenar los 10 parámetros en variables separadas
            param1, param2, param3, param4, param5, param6, param7, param8, param9, param10 = parametros

            # Puedes procesar los parámetros según sea necesario
            print(f"Parámetros recibidos: {parametros}")
            respuesta = "OK"
        else:
            print(f"Se esperaban 10 parámetros, pero se recibieron {len(parametros)}.")
            respuesta = "fail"

        # Enviar respuesta al cliente
        writer.write(respuesta.encode() + b'\n')
        await writer.drain()
    except Exception as e:
        print(f"Error al manejar la conexión desde {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Conexión cerrada con {addr}")

async def main():
    # Configuración SSL
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    servidor = await asyncio.start_server(
        manejar_cliente, '0.0.0.0', 8888, ssl=ssl_context)

    addr = servidor.sockets[0].getsockname()
    print(f'Servidor SSL escuchando en {addr}')

    async with servidor:
        await servidor.serve_forever()

asyncio.run(main())
