FROM python:3.6-alpine

LABEL version="1.0"
LABEL description="Scraping dentists data from findadentist.ada.org website."
LABEL maintainer="cpatrickalves@gmail.com"

COPY findadentist.py ./

COPY proxy_pool.py ./

COPY input.json ./

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "./findadentist.py", "input.json"]