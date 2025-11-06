import asyncio
import websockets

connected = set()

async def handler(websocket):
    print("Connected")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(message)
            for conn in connected:
                print(f"отравил {conn}")
                await conn.send(message)
    finally:
        connected.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Сервер запущен на ws://0.0.0.0:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
