import asyncio
import os
import logging

from functools import wraps
from aiohttp import web
from websockets import handshake
from websockets import WebSocketCommonProtocol

INDEX = open(os.path.join(os.path.dirname(__file__), 'index.html')).read()

class WebSocketResponse(web.Response):

    def __init__(self, request, switch_protocols):
        http11 = request._version == (1, 1)
        get_header = lambda k: dict(request.headers)[k.upper()]
        key = handshake.check_request(get_header)
        if not http11 or not key:
            super('Invalid WebSocket handshake.\n', status=400)
        else:
            headers = dict()
            set_header = headers.__setitem__
            handshake.build_response(set_header, key)
            self.switch_protocols = switch_protocols
            super().__init__(status=101, headers=headers)
            self._keep_alive = True
            request.transport.close = switch_protocols

@asyncio.coroutine
def testhandle(request):
    return web.Response(text='test handle')

@asyncio.coroutine
def handle(request):
    return web.Response(body=INDEX, content_type="text/html")


def websocket(handler):

    @asyncio.coroutine
    @wraps(handler)
    def wrapper(request, *args, **kwargs):
        transport = request.transport
        http_protocol = transport._protocol

        @asyncio.coroutine
        def run_ws_handler(ws):
            yield from handler(ws, request, *args, **kwargs)
            yield from ws.close()

        def switch_protocols():
            ws_protocol = WebSocketCommonProtocol()
            transport._protocol = ws_protocol
            ws_protocol.connection_made(transport)

            # Ensure aiohttp doesn't interfere.
            http_protocol.transport = None

            asyncio.async(run_ws_handler(ws_protocol))

        return WebSocketResponse(request, switch_protocols)

    return wrapper


@websocket
@asyncio.coroutine
def ws(ws, request):
    while ws.open:
        message = yield from ws.recv()
        if message:
            print(ws, request, message)
            yield from ws.send("Hello from aiohttp powered websocket!")


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', handle)
    app.router.add_route('GET', '/test', testhandle)
    app.router.add_route('GET', '/ws', ws)

    server = yield from loop.create_server(
        app.make_handler(),
        '0.0.0.0',
        8080
    )
    print("Server started at http://0.0.0.0:8080")
    return server


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()