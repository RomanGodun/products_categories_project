FROM python:3.10

WORKDIR /

COPY requirements requirements
RUN pip install -r requirements/requirements.txt

#std.err log level
ARG LOGGING_LEVEL="DEBUG"
#file log level
ARG LOGGING_DIR_LEVEL="DEBUG"
#folder for file logs
ARG LOG_DIR="logs"
ARG TZ=Europe/Moscow

ENV LOGGING_LEVEL=$LOGGING_LEVEL
ENV LOGGING_DIR_LEVEL=$LOGGING_DIR_LEVEL
ENV LOG_DIR=$LOG_DIR
ENV TZ=$TZ

RUN mkdir $LOG_DIR

COPY app app

COPY setup.py setup.py
RUN pip install -e .

CMD ["uvicorn", "app.api.main:app","--host","0.0.0.0"]