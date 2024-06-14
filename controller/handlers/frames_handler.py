import os
from time import sleep
from enum import Enum

from transport import database
from models import xclip


class FramesHandler:

    def __init__(self, model_interface) -> None:
        self.model = model_interface

    def run(self):
        while True:
            task = database.video_collection.find_one({'status_frames': database.StatusEnum.uploaded})
            if task:
                print(task)
                try:
                    database.update_task(task, {"status_frames": database.StatusEnum.processing})
                except Exception as err:
                    error = f"Task name {task.get('name')} not loaded \n Error: {err}"
                    print(error)
                    database.update_task(task, {"status_frames": database.StatusEnum.error, "error": error})
                    continue
                # call processing handler
                try:
                    model_inputs = xclip.XclipModelInputs(video_url=task["link"])
                    preds = self.model(model_inputs)
                    print(preds)
                    database.update_task(task, {"status_frames": database.StatusEnum.ready, "video_embedding": preds.embedding})
                except Exception as err:
                    error = f"Error while processing task name: {task.get('name')} \n Error: {err}"
                    print(error)
                    database.update_task(task, {"status_frames": database.StatusEnum.error, "error": error})
                    continue
            else:
                print(f"no task, sleeping {5.0}s ...")
                sleep(5.0)


def build_handler():
    model = xclip.XclipTritonModel(
            triton_url=os.environ['TRITON_URL'],
            triton_model_name="xclip-video-handler",
            model_version="1"
            )
    handler = FramesHandler(model)
    return handler

