from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shema import VideoResponse, UploadVideo

from search_engine import SearchEngine

search_engine_obj = SearchEngine()
app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
async def search(query: str) -> list[VideoResponse]:
    return search_engine_obj.search(query)

@app.get("/random_search")
async def random_search() -> list[VideoResponse]:
    return search_engine_obj.random_search()

@app.get("/search_similar")
async def search_similar(video_link: str) -> list[VideoResponse]:
    return search_engine_obj.search_similar(video_link)

@app.post("/add_video")
async def add_video(video: UploadVideo):
    return search_engine_obj.add_video(video)
