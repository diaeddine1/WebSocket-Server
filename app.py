import base64
import json
import websockets
import asyncio
import os
import http
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
                    response["frame_image"]=""
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
                    with open(image_label,"wb") as image_file:
                        image_file.write(image_data)
                    print(f"Image Saved as {image_label}")
                    with open(image_label,"rb") as image_file:
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


async def main():
    async def main():
        ip = "0.0.0.0"
        port = 8002
        async with websockets.serve(handler, ip, port=int(os.environ['PORT'])):
            print(f"WebSocket server running on ws://{ip}:{port}...")
            await asyncio.get_running_loop().create_future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
