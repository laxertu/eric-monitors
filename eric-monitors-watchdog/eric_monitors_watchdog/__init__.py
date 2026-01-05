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

class WatchDogChannel(AbstractChannel):
    def __init__(
            self,
            directory_to_monitor: str,
            recursive=True,
            stream_delay_seconds: int = 0,
            event_types: set[str] = ()
    ):
        super().__init__(stream_delay_seconds=stream_delay_seconds)
        self.__observer = Observer()
        self.__directory_to_monitor = directory_to_monitor
        self.__recursive = recursive
        self.__event_types = event_types

    def adapt(self, msg: MessageContract) -> MessageContract:
        return msg

    def start(self) -> None:
        self.__observer.schedule(WatchDogEventHandler(
            self, event_types=self.__event_types), self.__directory_to_monitor, recursive=self.__recursive
        )
        self.__observer.start()
        try:
            while self.__observer.is_alive():
                self.__observer.join(1)
        finally:
            self.__observer.stop()
            self.__observer.join()


class WatchDogEventHandler(FileSystemEventHandler):

    def __init__(self, channel: WatchDogChannel, event_types: set[str] | None = None):
        self.__channel = channel
        self.__event_types = event_types

    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.event_type in self.__event_types:
            self.__channel.broadcast(WatchDogMessage(event))
