import socketio
from app.videos_db import get_video_by_id

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*", logger=True, engineio_logger=True)

@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def status(event, _id):
    print(f'Event: {event}, SID: {_id}')
    video = await get_video_by_id(_id) 
    await sio.emit('status_response', 
                   {
                       "frames": video.get("status_frames"),
                       "speech": video.get("status_speech"),
                       "indexed":video.get("status_indexed"),
                       "faces":video.get("status_face_analysis"),
                       "indexed_faces":video.get("status_indexed_face"),
                       "duration_speech":video.get("duration_speech"),
                       "duration_indexed":video.get("duration_indexed"),
                       "duration_frames":video.get("duration_frames")
                       })
    
