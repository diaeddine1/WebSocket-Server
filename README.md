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
```
# Deploying the WebSocket Server on Render

This guide provides step-by-step instructions to deploy your Python WebSocket server to [Render](https://render.com).

## Prerequisites
- A Render account. Sign up at [Render](https://render.com) if you don’t have one.
- The server code in a Git repository (e.g., GitHub, GitLab, Bitbucket).

## Steps to Deploy

### 1. Log in to Render
- Visit [Render](https://render.com).
- Log in or sign up for an account.

---

### 2. Create a New Web Service
1. On the Render dashboard, click **“New”** > **“Web Service”**.
   
![image](https://github.com/user-attachments/assets/8bca330d-5617-480b-83c5-b8e53be47d14)

3. Select **“Connect a GitHub Repository”** or paste the Git repository URL manually.

![image](https://github.com/user-attachments/assets/96481398-36d8-471e-81cf-efd89d2642ee)

5. Allow Render to access your GitHub account if prompted.

---

### 3. Configure Deployment Settings
1. **Name Your Service**  
   Provide a name for your service (e.g., `websocket-server`).
    
2. **Setup your Configuration**
  Make sure you choose python 3 as your programming language
   
   ![image](https://github.com/user-attachments/assets/c0bcbc02-b949-4f40-b94e-41176d2e6533)

    Make sure you put python app.py as your start command and choose the free plan and finally click on deploy Web Service
   
   ![image](https://github.com/user-attachments/assets/ddcaad7a-ad98-4886-a6b9-f874d80c63a9)



