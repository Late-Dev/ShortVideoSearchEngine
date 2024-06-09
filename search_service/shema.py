from pydantic import BaseModel

class VideoResponse(BaseModel):
    link: str 
    description: str | None
