from eric_sse.entities import AbstractChannel
from eric_sse.message import MessageContract

from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

class WatchDogMessage(MessageContract):

    def __init__(self, event: FileSystemEvent):
        self.__event = event

    @property
    def type(self) -> str:
        return self.__event.event_type

    @property
    def payload(self) -> str:
        return self.__event.src_path

class WatchDogEventHandler(FileSystemEventHandler):

    def __init__(self, channel: AbstractChannel):
        self.__channel = channel

    def notify(self, event: FileSystemEvent) -> None:
        self.__channel.broadcast(WatchDogMessage(event))

class WatchDogChannel(AbstractChannel):
    def __init__(
            self,
            event_handler_class: WatchDogEventHandler.__class__,
            directory_to_monitor: str,
            recursive=True,
            stream_delay_seconds: int = 0
    ):
        super().__init__(stream_delay_seconds=stream_delay_seconds)
        self.__observer = Observer()
        self.__directory_to_monitor = directory_to_monitor
        self.__recursive = recursive
        self.__event_handler = event_handler_class(self)

    def adapt(self, msg: MessageContract) -> MessageContract:
        return msg

    def start(self) -> None:
        self.__observer.schedule(self.__event_handler, self.__directory_to_monitor, recursive=self.__recursive
        )
        self.__observer.start()
        try:
            while self.__observer.is_alive():
                self.__observer.join(1)
        finally:
            self.__observer.stop()
            self.__observer.join()

