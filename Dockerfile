FROM alpine as builder
WORKDIR /codebase
COPY . /codebase/
RUN rm /codebase/workers/database.py && mv /codebase/workers/docker_database.py /codebase/workers/database.py
RUN mv .env.example .env
RUN rm -rf .git gucotomap_data 2>/dev/null


FROM python:3.10-alpine
WORKDIR /Gucotomap
COPY --from=builder /codebase/ /Gucotomap/
RUN pip install -r requirements.txt
CMD [ "python", "bot.py" ]
