from mega import MegaApi
from modules.execute import execute
import modules.extensions
import os
import posixpath

class Mega:
    def __init__(self, email=None, password=None) -> None:
        cache_dir = "/cache/mega-http-server/"
        self.api = MegaApi('mega-http-server', cache_dir)
        session_key_path = posixpath.join(cache_dir, "session-key")

        if os.path.exists(session_key_path):
            print("Logging in with session key.")
            with open(session_key_path, "r") as file:
                session_key = file.read()
            execute(self.api.fastLogin, session_key)
        else:
            print("Logging in with email and password.")
            execute(self.api.login, os.environ.get('MEGA_EMAIL', email), os.environ.get('MEGA_PASSWORD', password))
            print("Dumping session key.")
            with open(session_key_path, "w+") as file:
                file.write(self.api.dumpSession())

        print("Fetching nodes.")
        execute(self.api.fetchNodes)
        
    def list_dir(self, path: str):
        path = '/' + path.lstrip('/')
        folder = self.api.getNodeByPath(path)
        folder = self.api.authorizeNode(folder)
        if folder:
            return [node.getName() for node in folder.getChildren()]
        else:
            return []
    
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
            
    def does_file_exist(self, path: str):
        path = '/' + path.lstrip('/')
        node = self.api.getNodeByPath(path)
        return node is not None
    
    def upload_file(self, mega_path: str, local_path: str, modification_time: int | None = None):
        mega_path = '/' + mega_path.lstrip('/')
        mega_dir_path = '/' + '/'.join(mega_path[1:].split('/')[0:-1])
        mega_dir_node = self.ensure_directory(mega_dir_path)
        
        if modification_time:
            self.api.startUpload(
                local_path,
                mega_dir_node,
                int(modification_time),
                True, # Delete file from local storage after upload.
                None)
        else:
            self.api.startUpload(
                local_path,
                mega_dir_node)
