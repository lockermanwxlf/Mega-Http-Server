from mega import MegaApi
from modules.execute import execute
import modules.extensions
import os

class Mega:
    def __init__(self, email=None, password=None) -> None:
        self.api = MegaApi('mega-http-server', '/app/cache/')
        execute(self.api.login, os.environ.get('MEGA_EMAIL', email), os.environ.get('MEGA_PASSWORD', password))
        execute(self.api.fetchNodes)
        
    def list_dir(self, path: str):
        path = '/' + path.lstrip('/')
        folder = self.api.getNodeByPath(path)
        folder = self.api.authorizeNode(folder)
        return [node.getName() for node in folder.getChildren()]
    
