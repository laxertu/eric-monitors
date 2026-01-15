import asyncio
import threading
import sys
from eric_monitors_watchdog import WatchDogChannel, WatchDogEventHandler
from watchdog.events import FileModifiedEvent

try:
    path = sys.argv[1]
except IndexError:
    print("Usage: python example_watchdog.py <path to monitor>")
    sys.exit(1)


class MyHandler(WatchDogEventHandler):
    """
    Extend base Handler to access to notify method, then define events you are interested to
    """
    def on_modified(self, event: FileModifiedEvent) -> None:
        self.notify(event)


async def main():
    c = WatchDogChannel(event_handler_class=MyHandler, directory_to_monitor=path)
    l = c.add_listener()
    l.start()

    t = threading.Thread(target=c.start)
    t.daemon = True
    t.start()

    print(f"Create of modify some file in {path}")

    try:
        async for m in c.message_stream(listener=l):
            print(f"[{m.type}] {m.payload}")
    except asyncio.CancelledError:
        print("\nExiting")
        exit(0)

if __name__ == '__main__':

    asyncio.run(main())