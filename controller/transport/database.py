import os
from asyncio import tasks
from enum import Enum

from pymongo import MongoClient


class StatusEnum(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    error = "error"


mongo_host = os.environ["MONGO_HOST"]
mongo_user = os.environ["MONGO_USER"]
mongo_pass = os.environ["MONGO_PASSWD"]

MONGO_DETAILS = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017"

client = MongoClient(MONGO_DETAILS)

database = client.data

video_collection = database.get_collection("videos")


def find_task(field: dict):
    task = video_collection.find_one(field)
    return task


def update_task(task: dict, t: dict):
    try:
        video_collection.update_one({"_id": task["_id"]}, {"$set": t}, upsert=True)
        return True
    except Exception as err:
        raise err


def replace_task(task: dict):
    try:
        video_collection.replace_one({"_id": task["_id"]}, task, upsert=True)
        return True
    except Exception as err:
        raise err


def find_all(field: dict):
    try:
        tasks = video_collection.find(field)
        return list(tasks)
    except:
        return False
