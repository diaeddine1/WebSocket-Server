import base64
import json
import websockets
import asyncio
import http
import os
import signal
import sys
from dotenv import load_dotenv
from websockets.asyncio.server import serve

load_dotenv()

# Store connected clients
connected_clients = set()

async def handler(websocket, path):
    # Add new connection to the set
    connected_clients.add(websocket)
    print("Client connected")

    try:
        async for message in websocket:
            try:
                payload = json.loads(message)  # Try to decode the message
                print(f"Payload received: {payload}")  # Debug print

                # Create a base response structure
                response = {
                    "status": "success",
                    "message": "Object detected"  # Default message for object detection
                }

                # Check if it's an object detection result
                if 'yolo_class_id' in payload:
                    print("Received object detection data:")
                    # Log object detection information
                    response["yolo_class_id"] = payload["yolo_class_id"]
                    response["yolo_id"] = payload["yolo_id"]
                    response["frame_image"] = ""
                    response["confidence"] = payload["confidence"]
                    response["frame_time"] = payload["frame_time"]
                    response["position_X"] = payload["position_X"]
                    response["position_Y"] = payload["position_Y"]
                else:
                    # If it's not object detection, handle it like a regular message
                    response["message"] = "Non-object detection message received"
                
                if 'frame_image' in payload:
                    print("The image Exists in the Payload")
                    base64_image = payload["frame_image"]
                    image_data = base64.b64decode(base64_image)
                    image_label = "Alert.jpg"
                    with open(image_label, "wb") as image_file:
                        image_file.write(image_data)
                    print(f"Image Saved as {image_label}")
                    with open(image_label, "rb") as image_file:
                        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
                        response["frame_image"] = image_base64 
                else:
                    response["frame_image"] = None 

                # Send the response to all connected clients
                for client in connected_clients:
                    try:
                        await client.send(json.dumps(response))
                        print(f"Sent response to {client}")  # Debug print
                    except websockets.exceptions.ConnectionClosed:
                        print(f"Client {client} is no longer connected")

            except json.JSONDecodeError:
                print("Failed to decode message")

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        # Client disconnected, clean up after iteration
        connected_clients.discard(websocket)  # Use discard to avoid KeyError if websocket isn't in set
        print("Client disconnected")

def health_check(connection, request):
    # Respond to health check or monitoring HTTP requests
    if request.path == "/healthz":
        return connection.respond(http.HTTPStatus.OK, "OK\n")
    # Respond to any other HTTP requests (e.g., HEAD or GET)
    elif request.method in ("HEAD", "GET"):
        return connection.respond(http.HTTPStatus.METHOD_NOT_ALLOWED, "WebSocket connection required\n")
    else:
        return connection.respond(http.HTTPStatus.BAD_REQUEST, "Bad request\n")

async def main():
    # Set the stop condition when receiving SIGTERM (only for Unix-like systems).
    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    print(sys.platform)

    if sys.platform == 'win32':
        print("windows")
    
    else :
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with serve(
        handler,
        host="",
        port=os.environ.get("PORT", 8000),
        process_request=health_check,
    ):
        await stop

if __name__ == "__main__":
    print("Starting the main function")
    asyncio.run(main())
    print("Main function running")
