# Desarrollado por HJ6DIE / Asorec
# APRS Bot con IA

Este proyecto implementa un bot que utiliza inteligencia artificial para comunicarse a través de la red APRS. El bot responde automáticamente a mensajes APRS utilizando la API de OpenAI (GPT) y limita las respuestas a 67 caracteres, como exige el protocolo APRS. Este bot es flexible y puede ser utilizado en cualquier evento o contexto donde se quiera integrar APRS con respuestas automatizadas.

## Funcionalidades
- **Recepción y envío de mensajes APRS**: El bot recibe mensajes APRS y genera respuestas automáticas a través de la API de OpenAI.
- **Historial de conversación por indicativo**: Mantiene un historial de conversación independiente para cada indicativo que interactúa con el bot.
- **Beacon**: Envía un beacon de activación periódicamente con la ubicación y comentarios del evento.
- **Gestión de comandos**: Permite reiniciar la conversación utilizando la palabra clave `nueva`.

## Requisitos

- **Python 3.x**
- **Bibliotecas**: 
  - `aprslib`
  - `openai`
  - `threading`
  
Puedes instalar las dependencias ejecutando:
```bash
pip install aprslib openai
```
# Configuración
## Variables de entorno
Para utilizar el bot, necesitarás una clave de la API de OpenAI. Por razones de seguridad, es recomendable que configures esta clave como una variable de entorno.
- **OPENAI_API_KEY:** Clave de la API de OpenAI (debe ser almacenada como variable de entorno).
Para configurar la variable de entorno (ejemplo en Linux/MacOS):
```bash
export OPENAI_API_KEY='tu-clave-aqui'
```
##Indicativo y APRS
Configura tu indicativo de APRS y contraseña directamente en el archivo de código:
```bash
CALLSIGN = "tu-indicativo"
APRS_PASS = "tu-contraseña"
```
## Ejecución
Para ejecutar el bot, una vez que todo esté configurado, simplemente corre el siguiente comando:
```bash
python aprs_bot.py
```
El bot comenzará a escuchar mensajes APRS y a responder automáticamente.
## Ejemplo de Uso
El bot responde preguntas sobre la historia de los scouts o cualquier otro tema que se le configure. Para iniciar una nueva conversación, basta con enviar el mensaje nueva.
## Licencia
Este proyecto está licenciado bajo los términos de la MIT License.
