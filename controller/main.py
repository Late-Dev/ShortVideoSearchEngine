from multiprocessing import Process

from handlers.frames_handler import build_handler as frames_handler_builder
from handlers.speech_handler import build_handler as speech_handler_builder
from handlers.search_handler import build_handler as search_handler_builder


all_handlers = [
    frames_handler_builder(),
    speech_handler_builder(),
    search_handler_builder()
]

def main():
    all_processes = [Process(target=handler.run) for handler in all_handlers]
    for process in all_processes:
       process.start()

    for process in all_processes:
       process.join()


if __name__ == "__main__":
    main()
