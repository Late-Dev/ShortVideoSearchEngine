from pydantic import BaseModel

class UploadVideoResponse(BaseModel):
    video_id: str

class RandomVideoResponse(BaseModel):
    link: str 
    description: str | None