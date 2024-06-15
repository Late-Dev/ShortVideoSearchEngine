from pydantic import BaseModel

class UploadVideoResponse(BaseModel):
    video_id: str

class VideoResponse(BaseModel):
    link: str 
    description: str | None
    
class VideoRequest(BaseModel):
    link: str 
    description: str | None