import asyncio
import logging
from eric_monitors.logger import LoggingChannel, EricHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

h = EricHandler(stream_delay_seconds=1)
logger.addHandler(h)

#---
l = h.channel.add_listener()
l.start()

logger.log(logging.INFO, 'log info')
logger.debug('debug')
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
logger.exception("exception")


async def main():
    async for m in h.channel.message_stream(listener=l):
        print(m)

if __name__ == '__main__':
    asyncio.run(main())


