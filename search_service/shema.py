from pydantic import BaseModel

class VideoResponse(BaseModel):
    link: str 
    description: str | None

class UploadVideo(BaseModel):
    link: str 
    description: str | None
    audio_text: str
    video_embedding: list[float]
