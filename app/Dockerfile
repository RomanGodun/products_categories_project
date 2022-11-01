FROM python:3.10

WORKDIR /app
COPY ./* /app/ 
RUN pip install -r requirements.txt
RUN mkdir /var/log/product_service


ENV LOG_G="20"
ENV TZ=Europe/Moscow

CMD ["uvicorn", "main:app","--host","0.0.0.0"]