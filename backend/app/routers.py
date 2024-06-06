from fastapi import APIRouter, Depends, Query, UploadFile
from app.schemas import UploadVideoResponse
from app.videos_db import add_video_data

router = APIRouter()


@router.post('/add_video', response_model=UploadVideoResponse)
async def add_video(file: UploadFile) -> UploadVideoResponse :
    """
    This endpoint uploads video to backend
    :returns id of video
    """
    return {"filename": file.filename}