from logging import Handler

from eric_sse.entities import AbstractChannel
from eric_sse.message import Message

class EricHandler(Handler):

    def __init__(self, channel: AbstractChannel, level=0):
        super().__init__(level)
        self.__channel = channel

    def emit(self, record):
        self.__channel.broadcast(Message(msg_type=record.levelname, msg_payload=self.format(record)))
