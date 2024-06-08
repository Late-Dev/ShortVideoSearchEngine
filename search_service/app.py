from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
async def search(query: str):
    return search_engine_obj.search(query)
