"""
This example uses https://laxertu.github.io/eric/prefabs.html#eric_sse.prefabs.SSEChannel to build an SSE channel

For example can be used to build that publish logs in real time on a Server Side Events stream

"""

import asyncio
import logging
from eric_monitors_python_logger import EricHandler
from eric_sse.prefabs import SSEChannel

logger = logging.getLogger(__name__)
sse_channel = SSEChannel()
logger.addHandler(EricHandler(sse_channel))
logger.setLevel(logging.DEBUG)

#---
l = sse_channel.add_listener()
l.start()

logger.log(logging.INFO, 'log info')
logger.debug('debug')
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
logger.exception("exception", exc_info=False)


async def main():
    input("Press any key tp start and Ctrl+C to exit")
    try:
        async for m in sse_channel.message_stream(listener=l):
            print(m)
    except asyncio.exceptions.CancelledError:
        print("\nThanks for watching :-)")

if __name__ == '__main__':
    asyncio.run(main())


