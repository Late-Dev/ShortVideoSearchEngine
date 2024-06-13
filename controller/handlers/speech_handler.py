import os
from time import sleep
from enum import Enum

from transport import database
from models import speech


class SpeechHandler:

    def __init__(self, model_interface) -> None:
        self.model = model_interface

    def run(self):
        while True:
            task = database.video_collection.find_one({'status_speech': database.StatusEnum.uploaded})
            if task:
                print(task)
                try:
                    database.update_task(task, {"status_speech": database.StatusEnum.processing})
                except Exception as err:
                    error = f"Task name {task.get('name')} not loaded \n Error: {err}"
                    print(error)
                    database.update_task(task, {"status_speech": database.StatusEnum.error, "error": error})
                    continue
                # call processing handler
                try:
                    model_inputs = speech.SpeechModelInputs(video_url=task["link"])
                    preds = self.model(model_inputs)
                    database.update_task(task, {"status_speech": database.StatusEnum.ready, "audio_text": preds.audio_text})
                except Exception as err:
                    error = f"Error while processing task name: {task.get('name')} \n Error: {err}"
                    print(error)
                    database.update_task(task, {"status_speech": database.StatusEnum.error, "error": error})
                    continue
            else:
                print(f"no task, sleeping {5.0}s ...")
                sleep(5.0)


def build_handler():
    model = speech.SpeechTritonModel(
            triton_url="10.10.66.25:8001",
            triton_model_name="speech-video-handler",
            model_version="1"
            )
    handler = SpeechHandler(model)
    return handler

