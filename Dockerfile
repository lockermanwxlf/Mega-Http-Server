FROM lockermanwxlf/mega-python-bindings

VOLUME [ "/app" ]

WORKDIR /app

RUN mkdir cache

CMD [ "sh", "start.sh" ]