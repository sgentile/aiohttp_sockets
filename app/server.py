import asyncio
import os
import logging

# from functools import wraps
from aiohttp import web
# from websockets import handshake
# from websockets import WebSocketCommonProtocol

INDEX = open(os.path.join(os.path.dirname(__file__), 'index.html')).read()

@asyncio.coroutine
def testhandle(request):
    return web.Response(text='test handle')

@asyncio.coroutine
def handle(request):
    return web.Response(body=INDEX, content_type="text/html")


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        print(msg.type)
        print(msg.data)
        ws.send_str(msg.data + '/answer')
        # if msg.type == WSMsgType.TEXT:
        #     if msg.data == 'close':
        #         await ws.close()
        #     else:
        #         ws.send_str(msg.data + '/answer')
        # elif msg.type == WSMsgType.ERROR:
        #     print('ws connection closed with exception %s' %
        #           ws.exception())

    print('websocket connection closed')

    return ws

app = web.Application()
app.router.add_route('GET', '/', handle)
app.router.add_route('GET', '/test', testhandle)
app.router.add_route('GET', '/ws', websocket_handler)
web.run_app(app)