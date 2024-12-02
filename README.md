# Python WebSocket Server

This repository contains a Python WebSocket server built with `websockets`. It supports real-time communication between clients and includes additional features like broadcasting messages, handling image payloads, and processing object detection data.

## Features
- **Real-time Communication**: Broadcasts messages to all connected clients.
- **Object Detection Integration**: Handles YOLO object detection data.
- **Image Processing**: Decodes, saves, and retransmits images in Base64 format.
- **Health Check**: Provides a `/healthz` endpoint to monitor server health.

## Requirements
- Python 3.8 or newer.
- Dependencies listed in `requirements.txt`.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/diaeddine1/WebSocket-Server.git
    cd WebsocketServer
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows: env\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory:
    ```plaintext
    PORT=8080  # Or any open port you have!
    ```

## Running Locally
Start the server with:
```bash
python app.py
