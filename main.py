import io
import logging
from flask import Flask, request, send_file

app = Flask(__name__)

# Configurar el registro para guardar los datos en un archivo de texto plano
logging.basicConfig(
    filename='accesos_ip.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Datos binarios de una imagen de 1x1 píxel transparente en formato PNG
TRANSPARENT_1X1_PNG = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc`\x00\x01\x00\x00\x0c\x00\x01\x04p\xdc\xe8\x00\x00\x00\x00IEND\xaeB`\x82'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Intentar obtener la IP real si el servidor está detrás de un proxy (como Cloudflare o Render)
    forwarded_for = request.headers.get('x-forwarded-for')
    if forwarded_for:
        client_ip = forwarded_for.split(',')[0].strip()
    else:
        client_ip = request.remote_addr

    # Capturar el navegador o dispositivo del usuario
    user_agent = request.headers.get('user-agent', 'Unknown')
    
    # Escribir los datos en el archivo 'accesos_ip.txt'
    logging.info(f"IP: {client_ip} | Ruta: /{path} | Navegador: {user_agent}")

    # Si se solicita específicamente la imagen, devolver el archivo PNG transparente
    if path == 'image.png':
        return send_file(
            io.BytesIO(TRANSPARENT_1X1_PNG),
            mimetype='image/png',
            download_name='image.png'
        )
    
    return "Servidor activo."

if __name__ == '__main__':
    # Arrancar la aplicación en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
