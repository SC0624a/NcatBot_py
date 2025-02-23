from importlib import reload
import asyncio
import msg_data
import websockets
import json
import fn


ws_url = 'ws://127.0.0.1:3001'   #自行换成你的连接

async def main():
    try:
        async with websockets.connect(f"{ws_url}/event") as ws:
            while True:
                message = await ws.recv()
                message = json.loads(message)
                await msg_data.messages(message)
                reload(fn)
    except Exception as e:
        print(f'{e}')
    finally:
        await asyncio.sleep(5)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        pass
