import os
from time import sleep, time
from enum import Enum

import requests

from transport import database


class SearchFaceHandler:

    def __init__(self) -> None:
        pass

    def run(self):
        while True:
            task = database.video_collection.find_one({
                'status_face_analysis': database.StatusEnum.ready,
                'status_indexed_face': database.StatusEnum.uploaded
            })
            if task:
                try:
                    start_time = time()
                    data = {
                        'link': task['link'],
                        'description': task['description'],
                        'video_face_embeddings': task['face_embeddings']
                    }
                    response = requests.post(f'{os.environ["SEARCH_SERVICE_FACE"]}/add_video', json=data)
                    if response.status_code == 200:
                        database.update_task(task, {
                            "status_indexed_face": database.StatusEnum.ready,
                            "duration_indexed_face": time() - start_time
                        })
                    else:
                        database.update_task(task, {"status_indexed_face": database.StatusEnum.error, "error": response.text})
                except Exception as err:
                    error = f"Error while processing task name: {task.get('name')} \n Error: {err}"
                    print(error)
                    database.update_task(task, {"status_indexed_face": database.StatusEnum.error, "error": error})
                    continue
            else:
                print(f"no task, sleeping {5.0}s ...")
                sleep(5.0)


def build_handler():
    handler = SearchFaceHandler()
    return handler

