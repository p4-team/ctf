import sys
import json
import asyncio
import websockets

URI = 'ws://harmony-1.hackable.software:3380/chat'

async def register(ws, name: str) -> str:
    await ws.send(json.dumps({'type': 'register', 'displayName': name}))
    
    uid_msg = await ws.recv()
    parsed_msg = json.loads(uid_msg)
    if not 'uid' in parsed_msg:
        print(parsed_msg, name)
    return parsed_msg['uid']

def create_channel(name: str) -> str:
    return json.dumps({'type': 'new-channel', 'name': name})

def invite(uid: str) -> str:
    global cid
    return json.dumps({'type': 'invite', 'chId': cid, 'uid': uid})

def message(msg: str) -> str:
    global cid
    return json.dumps({'type': 'message', 'chId': cid, 'msg': msg})



def parse_line(line: str):
    line = line.rstrip()
    if line == '':
        return ('random_name', '')
    parts = line.split(': ')
    return (parts[0], ':'.join(parts[1:]))

cid = ''

async def send_line(line: str, main_ws):
    global cid
    payload_name, payload_msg = parse_line(line)
    async with websockets.connect(URI) as ws:
        print('Payload WS connected!')
        uid = await register(ws, payload_name)
        await ws.recv() # welcome message
        await main_ws.send(invite(uid))
        await main_ws.recv() # "Invited {uname} to channel {cname}."
        await ws.recv() # joined message
        await ws.send(message(payload_msg))
        print(await ws.recv())

async def hello():
    global cid
    lines = []
    with open(sys.argv[1]) as payload:
        lines = payload.readlines()
        print(lines)
    async with websockets.connect(URI) as main_ws:
        print('Main WS connected!')
        # register main websocket
        payload_name, payload_msg = parse_line(lines[0])

        uid = await register(main_ws, payload_name)

        await main_ws.recv() # welcome message - skip

        # create payload channel
        await main_ws.send(create_channel('payload'))

        joined_msg = await main_ws.recv()
        cid = json.loads(joined_msg)['channels'][0]['chId']

        # send first line of payload
        await main_ws.send(message(payload_msg))
        print(await main_ws.recv())

        for line in lines[1:]:
            await send_line(line, main_ws)

        print(f'http://harmony-1.hackable.software:3380/logs/{uid}/{cid}')

asyncio.get_event_loop().run_until_complete(hello())
