import motor.motor_asyncio
from enum import Enum
import os 
from bson.objectid import ObjectId


from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

mongo_user = os.environ["MONGO_USER"]
mongo_passwd = os.environ["MONGO_PASSWD"]
mongo_host = os.environ["MONGO_HOST"]
MONGO_DETAILS = f"mongodb://{mongo_user}:{mongo_passwd}@{mongo_host}:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.data
video_collection = database.get_collection("videos")

class StatusEnum(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    error = "error"

async def add_video_data(data):
    video = {}
    video["status_frames"] = StatusEnum.uploaded
    video["status_speech"] = StatusEnum.uploaded
    video["status_face_analysis"] = StatusEnum.uploaded
    video["status_indexed_face"] = StatusEnum.uploaded
    video["status_indexed"] = StatusEnum.uploaded
    video["link"] = data.link
    video["description"] = data.description
    _id = await video_collection.insert_one(video)
    return _id.inserted_id

async def get_random_video_data():
    pipeline = [
        {"$sample": {"size": 2}}  # Получаем 2 случайных документ
    ] 
    result = []
    async for doc in video_collection.aggregate(pipeline):
        result.append({"link": doc.get("link"), "description": doc.get("description")})
        # return doc
    return result

async def get_video_by_id(id: str):
    video = await video_collection.find_one({"_id": ObjectId(id)} )
    if video is not None:
        return video
    else:
        assert LookupError("Video not found")