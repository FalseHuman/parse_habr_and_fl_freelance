import asyncio


class Mainloop:
    def __init__(self):
        self.mainloop = asyncio.get_event_loop()

    def start_mainloop(self, coroutine) -> None:
        try:
            self.mainloop.run_until_complete(coroutine)
        except KeyboardInterrupt:
            self.mainloop.close()
