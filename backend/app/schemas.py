from pydantic import BaseModel

class UploadVideoResponse(BaseModel):
    video_id: str
