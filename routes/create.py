import asyncio
from aiohttp import web

from client import ClientTCPSocket
from server import GameServer
from room import GameRoom, GamePlayer

async def create(request: web.Request):
    body = await request.json()
    server = GameServer.instance()
    client = server.find_client(body['login'])

    if not client:
        # Client is not connected via the TCP port
        return web.Response(status=400)

    host = GamePlayer(client, body['name'])

    room = GameRoom(host, body['size'], body['selection'], body['medal'])
    asyncio.create_task(room.initialize_maplist())
    server.rooms.append(room)

    return web.Response(text=room.code)