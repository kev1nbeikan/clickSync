import asyncio
import websockets
import ctypes
import time
import aioconsole

SERVER_URI = "ws://localhost:8765"
VK_MEDIA_PLAY_PAUSE = 0xB3
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

def send_media_play_pause():
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

async def listen_server(websocket):
    async for message in websocket:
        if message == "play":
            print("Получена команда: старт проигрывания")
            send_media_play_pause()

async def send_play(websocket):
    while True:
        await aioconsole.ainput("Нажмите Enter для старта >>> ")
        print("Локально: стартуем проигрывание, отправляем команду.")
        send_media_play_pause()
        await websocket.send("play")

async def client():
    async with websockets.connect(SERVER_URI) as websocket:
        print("Подключено к серверу.")
        await asyncio.gather(
            listen_server(websocket),
            send_play(websocket)
        )

if __name__ == "__main__":
    asyncio.run(client())
