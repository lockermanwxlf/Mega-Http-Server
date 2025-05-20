FROM lockermanwxlf/mega-python-bindings

EXPOSE 8080

VOLUME [ "/cache/mega-http-server" ]

WORKDIR /app

COPY src/requirements.txt .

RUN python -m venv --system-site-packages .venv && \
    .venv/bin/pip install -r requirements.txt

COPY src/. .

RUN mkdir /cache/mega-http-server -p

CMD [ ".venv/bin/python", "-u", "main.py" ]