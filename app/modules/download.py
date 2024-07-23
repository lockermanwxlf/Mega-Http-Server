import os
from fake_useragent import FakeUserAgent
from requests import Session
from requests.exceptions import ChunkedEncodingError

def get_current_size(path: str):
    return os.path.getsize(path) if os.path.exists(path) else 0

user_agent = FakeUserAgent()
session = Session()

def download_to_file(url: str, path: str):
    global user_agent, session
    current_size = get_current_size(path)
    headers = {
        'User-Agent': user_agent.random
    }
    with session.get(
        url=url,
        headers=headers,
        stream=True
    ) as response:
        content_length = int(response.headers['Content-Length'])
    while current_size < content_length:
        headers['User-Agent'] = user_agent.random
        headers['Range'] = f'bytes={current_size}-{content_length}'
        with session.get(
            url=url,
            headers=headers,
            stream=True
        ) as response:
            if response.ok:
                with open(path, 'ab+') as out:
                    try:
                        for block in response.iter_content(2**10):
                            if not block:
                                break
                            out.write(block)
                    except ChunkedEncodingError:
                        pass
            current_size = get_current_size(path)
