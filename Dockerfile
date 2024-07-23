FROM lockermanwxlf/mega-python-bindings

VOLUME [ "/app" ]

WORKDIR /app

COPY app/requirements.txt .

RUN pip3 install -r requirements.txt

RUN mkdir cache

CMD [ "sh", "start.sh" ]