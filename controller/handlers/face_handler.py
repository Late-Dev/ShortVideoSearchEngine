import os
from time import sleep
from enum import Enum

from transport import database
from models import face


class FaceAnalysisHandler:

    def __init__(self, model_interface) -> None:
        self.model = model_interface

    def run(self):
        while True:
            task = database.video_collection.find_one({'status_face_analysis': database.StatusEnum.uploaded})
            if task:
                print(task)
                try:
                    database.update_task(task, {"status_face_analysis": database.StatusEnum.processing})
                except Exception as err:
                    error = f"Task name {task.get('name')} not loaded \n Error: {err}"
                    print(error)
                    database.update_task(task, {"status_face_analysis": database.StatusEnum.error, "error": error})
                    continue
                # call processing handler
                try:
                    model_inputs = face.FaceAnalysisModelInputs(video_url=task["link"])
                    preds = self.model(model_inputs)
                    database.update_task(task, {"status_face_analysis": database.StatusEnum.ready, "face_embeddings": preds.embeddings})
                except Exception as err:
                    error = f"Error while processing task name: {task.get('name')} \n Error: {err}"
                    print(error)
                    database.update_task(task, {"status_face_analysis": database.StatusEnum.error, "error": error})
                    continue
            else:
                print(f"no task, sleeping {5.0}s ...")
                sleep(5.0)


def build_handler():
    model = face.FaceAnalysisTritonModel(
            triton_url=os.environ['TRITON_URL'],
            triton_model_name="face-analysis",
            model_version="1"
            )
    handler = FaceAnalysisHandler(model)
    return handler