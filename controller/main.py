from multiprocessing import Process

from handlers.frames_handler import FrameHandler

all_handlers = [
    FrameHandler()
]

def main():
    all_processes = [Process(target=handler.run) for handler in all_handlers]
    for process in all_processes:
       process.start()

    for process in all_processes:
       process.join()


if __name__ == "__main__":
    main()
