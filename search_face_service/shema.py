from pydantic import BaseModel

class VideoResponse(BaseModel):
    link: str 
    description: str | None

class UploadVideo(BaseModel):
    link: str 
    description: str | None
    video_face_embeddings: list[list]
