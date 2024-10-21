# APRS Bot con IA para JOTA-JOTI 2024

Este proyecto implementa un bot que utiliza inteligencia artificial para comunicarse a través de la red APRS. El bot responde automáticamente a mensajes APRS utilizando la API de OpenAI (GPT) y limita las respuestas a 67 caracteres, como exige el protocolo APRS.

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
