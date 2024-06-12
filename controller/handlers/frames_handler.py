import os
from time import sleep
from enum import Enum

from pymongo import MongoClient


class StatusEnum(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    error = "error"


class FramesHandler:
    def __init__(self):
        mongo_host = os.environ["MONGO_HOST"]
        mongo_user = os.environ["MONGO_USER"]
        mongo_pass = os.environ["MONGO_PASSWD"]

        MONGO_DETAILS = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017"

        client = MongoClient(MONGO_DETAILS)

        database = client.data

        self.video_collection = database.get_collection("videos")

    def run(self):
        while True:
            task = self.video_collection.find_one({'status_frames': StatusEnum.uploaded})
            if task:
                pass

            sleep(5.0)


