from pydantic import BaseModel

class UploadVideoResponse(BaseModel):
    filename: str
