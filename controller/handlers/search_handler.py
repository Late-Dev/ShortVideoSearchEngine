import os
from time import sleep
from enum import Enum

import requests

from transport import database


class SearchHandler:

    def __init__(self) -> None:
        pass

    def run(self):
        while True:
            task = database.video_collection.find_one({
                'status_speech': database.StatusEnum.ready,
                'status_frames': database.StatusEnum.ready,
                'status_indexed': False
            })
            if task:
                try:
                    data = {
                        'link': task['link'],
                        'description': task['description'],
                        'audio_text': task['audio_text'],
                        'video_embedding': task['video_embedding']
                    }
                    response = requests.post(f'{os.environ["SEARCH_SERVICE"]}/add_video', json=data)
                    if response.status_code == 200:
                        database.update_task(task, {"status_indexed": database.StatusEnum.ready})
                    else:
                        database.update_task(task, {"status_indexed": database.StatusEnum.error, "error": response.text})
                except Exception as err:
                    error = f"Error while processing task name: {task.get('name')} \n Error: {err}"
                    print(error)
                    database.update_task(task, {"status_indexed": database.StatusEnum.error, "error": error})
                    continue
            else:
                print(f"no task, sleeping {5.0}s ...")
                sleep(5.0)


def build_handler():
    handler = SearchHandler()
    return handler

