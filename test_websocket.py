import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Send a message
        await websocket.send("Hello Server!")
        print("Sent: Hello Server!")
        
        # Receive response
        response = await websocket.recv()
        print(f"Received: {response}")

if __name__ == "__main__":
    asyncio.run(test_websocket()) 