import asyncio
import websockets
import base64
import mss
import numpy as np
import cv2

# WebSocket URL (adjust to your server's address)
WEBSOCKET_URL = "ws://localhost:8000/ws/client-stream/client_001/"

async def capture_and_stream():
    """Captures the screen and streams it via WebSocket."""
    while True:
        try:
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                print("Connected to WebSocket server.")

                # Initialize screen capture
                with mss.mss() as sct:
                    # Define the monitor to capture (use sct.monitors[1] for the primary monitor)
                    monitor = sct.monitors[1]

                    while True:
                        # Capture the screen
                        screenshot = sct.grab(monitor)

                        # Convert the raw RGB data into a numpy array
                        img_array = np.array(screenshot)

                        # Convert the numpy array to a JPEG image
                        _, buffer = cv2.imencode('.jpg', img_array)

                        # Convert the JPEG buffer to a base64 string
                        base64_frame = base64.b64encode(buffer).decode('utf-8')

                        # Send the frame to the WebSocket server
                        await websocket.send(base64_frame)

                        # Add a small delay to control the frame rate
                        await asyncio.sleep(0.03)  # Adjust frame rate as needed

        except websockets.ConnectionClosedError as e:
            print(f"Connection closed. Retrying in 5 seconds... Error: {e}")
            await asyncio.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await asyncio.sleep(5)  # Wait before retrying

async def main():
    await capture_and_stream()

if __name__ == "__main__":
    asyncio.run(main())
