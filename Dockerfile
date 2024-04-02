FROM python:3.10-alpine
WORKDIR /Gucotomap
COPY . /Gucotomap/
RUN rm /Gucotomap/workers/database.py && mv /Gucotomap/workers/docker_database.py /Gucotomap/workers/database.py
RUN pip install -r requirements.txt
CMD [ "python", "bot.py" ]


# winpty docker run \
# -e BOT_TOKEN=6905062343:AAGn8bhe62uqj4ha2mtk8cAbn46GgUa0R5M \
# --mount type=bind,source=$(pwd),destination=/Gucotomap_bot-main/.env \
# gucotomap:3