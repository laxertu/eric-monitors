import asyncio
import logging
from eric_monitors_python_logger import EricHandler


logger = logging.getLogger(__name__)

h = EricHandler()
logger.addHandler(h)
logger.setLevel(logging.DEBUG)

#---
l = h.channel.add_listener()
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
        async for m in h.channel.message_stream(listener=l):
            print(f"[{m.type}] {m.payload}")
    except asyncio.exceptions.CancelledError:
        print("\nThank you for watching :-)")

if __name__ == '__main__':
    asyncio.run(main())


