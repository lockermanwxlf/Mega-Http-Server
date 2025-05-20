from mega import MegaRequestListener
from threading import Event
from typing import Callable

class RequestListener(MegaRequestListener):
    def __init__(self):
        self.event = Event()
        super().__init__()
        
    def onRequestFinish(self, api, request, e):
        self.event.set()

async def execute_async(function: Callable, *args: any):
    listener = RequestListener()
    function(*args, listener)
    listener.event.wait()
    
def execute(function: Callable, *args: any):
    listener = RequestListener()
    function(*args, listener)
    listener.event.wait()
