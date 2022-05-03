FROM python

RUN pip install discord

COPY . /app
WORKDIR /app

ENTRYPOINT ["python3","bot.py"]
