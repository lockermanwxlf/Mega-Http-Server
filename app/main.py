from flask import Flask, Response, request
from modules.mega import Mega
from modules.download import download_to_file

mega = Mega()

app = Flask(__name__)

@app.get('/file')
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

@app.put('/file')
def upload_file():
    # Return 400 if mega_path or file is missing.
    if 'mega_path' not in request.form:
        return Response('Form missing \'mega_path\'.', 400)
    if 'file' not in request.files:
        return Response('Files missing \'file\'.', 400)
      
    # Get intended file name from mega_path.
    mega_path = request.form['mega_path']
    filename = mega_path.split('/')[-1]
    filepath = f'/tmp/{filename}'
    
    # Save uploaded file.
    file = request.files['file']
    file.save(filepath)
    
    # Upload file.
    mega.upload_file(mega_path, filepath, request.form.get('modification_time'))

    return Response('', 200)

@app.post('/file')
def download_file():
    # Return 400 if mega_path or content_url is missing.
    for required in ['mega_path', 'content_url']:
        if required not in request.form:
            return Response(f'Form missing \'{required}\'.', 400)
        
    # Get intended file name from mega_path.
    mega_path = request.form['mega_path']
    filename = mega_path.split('/')[-1]
    filepath = f'/tmp/{filename}'

    # Download file from content_url.
    download_to_file(request.form['content_url'], filepath)
    
    # Upload file
    mega.upload_file(mega_path, filepath, request.form.get('modification_time'))
    
    return Response('', 200)

@app.get('/folder')
def list_folder():
    # Return 400 if path is missing.
    if 'path' not in request.args:
        return Response('Form missing \'path\'.', 400)
    
    # Return result of list_dir.
    return mega.list_dir(request.args['path'])

# Start server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, use_reloader=False)
