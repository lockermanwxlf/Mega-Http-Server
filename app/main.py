from flask import Flask, Response, request
from modules.mega import Mega

mega = Mega()

app = Flask(__name__)

@app.get("file")
def check_file():
    # Return 400 if path is missing from query params.
    if 'path' not in request.args:
        return Response('Missing path argument', 400)
    
    # Only a status code is returned to indicate existence.
    path = request.args['path']
    if mega.does_file_exist(path):
        return Response('', 200)
    else:
        return Response('', 404)
