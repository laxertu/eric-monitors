import asyncio
import threading
import sys
from eric_monitors_watchdog import WatchDogChannel, WatchDogEventHandler
from watchdog.events import EVENT_TYPE_MODIFIED, DirModifiedEvent, FileModifiedEvent

try:
    path = sys.argv[1]
except IndexError:
    print("Usage: python example_wd.py <path>")
    sys.exit(1)

class MyHandler(WatchDogEventHandler):

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        self.notify(event)

c = WatchDogChannel(event_handler_class=MyHandler, directory_to_monitor=path)
l = c.add_listener()
l.start()

async def main():
    t = threading.Thread(target=c.start)
    t.daemon = True
    t.start()

    async for m in c.message_stream(listener=l):
        print(f"[{m.type}] {m.payload}")

if __name__ == '__main__':

    asyncio.run(main())