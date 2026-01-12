from logging import Handler

from eric_sse.entities import AbstractChannel
from eric_sse.message import MessageContract, Message

class LoggingChannel(AbstractChannel):

    def adapt(self, msg: MessageContract) -> MessageContract:
        return msg

class EricHandler(Handler):

    def __init__(self, level=0, stream_delay_seconds=0):
        super().__init__(level)
        self.__channel = LoggingChannel(stream_delay_seconds=stream_delay_seconds)

    @property
    def channel(self) -> AbstractChannel:
        return self.__channel

    def emit(self, record):
        self.__channel.broadcast(Message(msg_type=record.levelname, msg_payload=self.format(record)))
