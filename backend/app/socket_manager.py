import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*", logger=True, engineio_logger=True)

@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

@sio.on('*')
async def catch_all(event, sid, data):
    print(f'Event: {event}, SID: {sid}, Data: {data}')