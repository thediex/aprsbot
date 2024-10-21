import aprslib
import threading
import openai
import time
import os

# === Configuración de constantes ===
# La clave de API debe almacenarse en una variable de entorno para seguridad
openai.api_key = os.getenv('OPENAI_API_KEY')  # Debes configurar esta variable de entorno

# Constantes de configuración APRS
CALLSIGN = "XXXXXX"  # Indicativo
APRS_PASS = "XXXXX"    # Contraseña APRS-IS (debe estar almacenada de forma segura)
APRS_SERVER = "soam.aprs2.net"
APRS_PORT = 14580
BEACON_LAT = 4.8356999
BEACON_LON = -75.6718446
BEACON_COMMENT = "IA APRS JOTA-JOTI 2024 Asorec"

# Inicializar conexión APRS-IS
ais = aprslib.IS(CALLSIGN, passwd=APRS_PASS)
ais.set_server(APRS_SERVER, APRS_PORT)
ais.connect()

# Diccionario para almacenar los historiales de conversación por indicativo
memoria_indicativos = {}

# Conjunto para almacenar los IDs de mensajes procesados (indicativo + msgNo)
mensajes_procesados = set()

# === Funciones ===

# Función para convertir coordenadas decimales a formato APRS (grados y minutos)
def convertir_a_aprs(lat, lon):
    """Convierte coordenadas decimales a formato APRS."""
    lat_grados = int(abs(lat))
    lat_minutos = (abs(lat) - lat_grados) * 60
    lat_direccion = 'N' if lat >= 0 else 'S'

    lon_grados = int(abs(lon))
    lon_minutos = (abs(lon) - lon_grados) * 60
    lon_direccion = 'E' if lon >= 0 else 'W'

    aprs_lat = f"{lat_grados:02d}{lat_minutos:05.2f}{lat_direccion}"
    aprs_lon = f"{lon_grados:03d}{lon_minutos:05.2f}{lon_direccion}"
    
    return aprs_lat, aprs_lon

# Función para manejar el chat con GPT-4
def chat_with_gpt(prompt, indicativo):
    """Genera una respuesta utilizando el modelo GPT basado en la conversación anterior."""
    try:
        if indicativo not in memoria_indicativos:
            # Crear historial para el nuevo indicativo
            memoria_indicativos[indicativo] = [
                {"role": "system", "content": (
                    "Eres un bot que te harás pasar por Lord Robert Baden-Powell en conmemoración "
                    "a los scouts para el evento del jota-joti 2024. Nunca debes exceder los 67 "
                    "caracteres en las respuestas debido a las limitaciones de APRS.") 
                }
            ]
        
        # Añadir el mensaje del usuario al historial correspondiente al indicativo
        memoria_indicativos[indicativo].append({"role": "user", "content": prompt})
        
        # Llama a la API de OpenAI para generar una respuesta
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Usa el modelo GPT según disponibilidad
            messages=memoria_indicativos[indicativo]
        )
        
        # Obtén la respuesta del asistente
        reply = response['choices'][0]['message']['content']
        
        # Añadir la respuesta del asistente al historial
        memoria_indicativos[indicativo].append({"role": "assistant", "content": reply})
        
        # Devuelve la respuesta generada
        return reply
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return "Hubo un error, intenta de nuevo."

# Función para enviar el ID del mensaje como ACK
def enviar_ack(destinatario, msg_id):
    """Envía un paquete ACK al destinatario en respuesta a un mensaje recibido."""
    ack_packet = f"{CALLSIGN}>APFIIO,qAC,APRSFI::{destinatario}:ack{msg_id}"
    print(f"Enviando ACK: {ack_packet}")
    ais.sendall(ack_packet)

# Función para recibir mensajes
def recibir_mensajes():
    """Escucha y procesa los mensajes entrantes de APRS."""
    def callback(packet):
        if packet.get('format') == 'message':
            indicativo = packet['from']
            mensaje = packet['message_text']
            msg_no = packet.get('msgNo')  # Obtener el ID del mensaje

            # Crear una clave única combinando el indicativo y el msgNo
            clave_mensaje = f"{indicativo}-{msg_no}"

            # Verificar si el mensaje ya fue procesado
            if clave_mensaje in mensajes_procesados:
                return  # Ignorar el mensaje duplicado

            print(f"Mensaje de {indicativo}: {mensaje} (ID: {msg_no})")

            # Marcar el mensaje como procesado
            mensajes_procesados.add(clave_mensaje)

            # Verificar si el usuario quiere iniciar una nueva conversación
            if mensaje.strip().lower() == "nueva":
                memoria_indicativos.pop(indicativo, None)  # Borrar la memoria
                ais.sendall(f"{CALLSIGN}>APRS::{indicativo}: Conversación reiniciada.")
            else:
                # Generar respuesta automática con GPT
                respuesta = chat_with_gpt(mensaje, indicativo)
                respuesta_packet = f"{CALLSIGN}>APRS::{indicativo}:   {respuesta[:67]}"
                ais.sendall(respuesta_packet)
                print(f"Respuesta enviada a {indicativo}: {respuesta}")
            
            # Enviar ACK utilizando el msgNo
            if msg_no:
                enviar_ack(indicativo, msg_no)

    # Consumir paquetes de la red APRS
    ais.consumer(callback, raw=False)

# Enviar beacon de activación cada 2 minutos
def enviar_beacon():
    """Envía un beacon de activación periódicamente."""
    while True:
        latitude, longitude = convertir_a_aprs(BEACON_LAT, BEACON_LON)
        beacon_packet = f"{CALLSIGN}>APRS,TCPIP*:={latitude}/{longitude}-{BEACON_COMMENT}"
        print(f"Beacon enviado: {beacon_packet}")
        ais.sendall(beacon_packet)
        time.sleep(120)  # Esperar 2 minutos antes de enviar el siguiente beacon

# === Hilos de ejecución ===

# Iniciar la recepción de mensajes en un hilo separado
threading.Thread(target=recibir_mensajes).start()

# Iniciar el envío de beacon en un hilo separado
threading.Thread(target=enviar_beacon).start()
