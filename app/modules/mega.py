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
    
    def ensure_directory(self, path: str):
        path = '/' + path.rstrip('/')
        node = self.api.getNodeByPath(path)
        if node is None:
            node = self.api.getRootNode()
            for name in path.split('/')[1:]:
                next_node = self.api.getNodeByPath(name, node)
                if next_node is None:
                    execute(self.api.createFolder, name, node)
                    next_node = self.api.getNodeByPath(name, node)
                node = next_node
        return node
            