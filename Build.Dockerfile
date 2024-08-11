FROM lockermanwxlf/mega-python-bindings

EXPOSE 80

WORKDIR /app

COPY app/ .

RUN pip3 install -r requirements.txt

RUN mkdir /cache

CMD [ "sh", "start.sh" ]