from fastapi import APIRouter, Depends, Query, UploadFile

from app.schemas import (
    UploadVideoResponse, 
    RandomVideoResponse
    ) 

from app.videos_db import (
    add_video_data,
    get_random_video_data
    )

router = APIRouter()


@router.post('/add_video', response_model=UploadVideoResponse)
async def add_video(file: UploadFile) -> UploadVideoResponse:
    """
    This endpoint uploads video to backend
    :returns id of video
    """
    video_id = await add_video_data({}, {"link": "https://cdn-st.rutubelist.ru/media/b1/3a/0f53a71c4213a9824578b7d49bd4/fhd.mp4", "description": "nothing"})
    return {"video_id": str(video_id)}


@router.get('/get_random_video', response_model = list[RandomVideoResponse])
async def get_random_video() -> list[RandomVideoResponse]:
    """
    This endpoint returns random video
    :returns id of video
    """
    sample = await get_random_video_data()
    return sample


