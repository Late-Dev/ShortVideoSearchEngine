import aiohttp
from fastapi import APIRouter, Depends, Query, UploadFile

from app.schemas import (
    UploadVideoResponse, 
    VideoResponse,
    VideoRequest
    ) 

from app.videos_db import (
    add_video_data,
    get_random_video_data
    )

router = APIRouter()


@router.post('/index', response_model=UploadVideoResponse)
async def add_video(payload: VideoRequest) -> UploadVideoResponse: 
    """
    This endpoint uploads link of video and description to backend
    :returns id of video in mongo which can be used to watch processing
    """

    video_id = await add_video_data(payload)
    return {"video_id": str(video_id)}


@router.get('/get_random_video', response_model = list[VideoResponse])
async def get_random_video() -> list[VideoResponse]:
    """
    This endpoint returns random video
    :returns id of video
    """
    sample = await get_random_video_data()
    return sample


@router.get('/search', response_model = list[VideoResponse])
async def get_video_by_query(text: str) -> list[VideoResponse]:
    result = []
    async with aiohttp.ClientSession() as session:
        async with session.get('http://search-face-service/search_face', params={'query': text}) as response:

            result += await response.json()

    async with aiohttp.ClientSession() as session:
        async with session.get('http://search-service/search', params={'query': text}) as response:

            result += await response.json()
    return result

@router.get('/search_similar', response_model = list[VideoResponse])
async def get_video_by_similar(video_link: str) -> list[VideoResponse]:

    async with aiohttp.ClientSession() as session:
        async with session.get('http://search-service/search_similar', params={'video_link': video_link}) as response:

            result = await response.json()
    return result

