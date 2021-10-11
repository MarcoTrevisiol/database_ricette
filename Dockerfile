FROM python:slim

RUN apt-get update && apt-get install -y gcc locales && \
	sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen && \
	dpkg-reconfigure --frontend=noninteractive locales

WORKDIR /usr/local/database_ricette/telegram_bot

COPY telegram_bot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram_bot/ .
COPY catalogo_ricette.json ../catalogo_ricette.json

CMD [ "python", "./botter.py" ]

