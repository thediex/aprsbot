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

