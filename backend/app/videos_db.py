import motor.motor_asyncio
from enum import Enum
import os 
mongo_user = os.environ["MONGO_USER"]
mongo_passwd = os.environ["MONGO_PASSWD"]
mongo_host = os.environ["MONGO_HOST"]
MONGO_DETAILS = f"mongodb://{mongo_user}:{mongo_passwd}@{mongo_host}:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.data
vodeo_collection = database.get_collection("videos")

class StatusEnum(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    error = "error"


async def add_video_data(video, payload):
    video["status"] = StatusEnum.uploaded
    video["link"] = payload
    _id = await vodeo_collection.insert_one(video)
    print(_id.inserted_id)
    return _id.inserted_id