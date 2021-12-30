FROM python:slim

RUN apt-get update && apt-get install -y gcc locales && \
	sed -i -e 's/# it_IT.UTF-8 UTF-8/it_IT.UTF-8 UTF-8/' /etc/locale.gen && \
	dpkg-reconfigure --frontend=noninteractive locales

WORKDIR /usr/local/telegram_bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
ENV PERSISTENCE=/var/local/persistence
ENV DATABASE=/var/local/database
RUN sed -i -e "s|persistence=.*$|persistence=${PERSISTENCE}/persistence.pickle|" coordinates && \
    sed -i -e "s|'bot.log'|'${PERSISTENCE}/bot.log'|" logger.ini && \
    sed -i -e "s|database=.*$|database=${DATABASE}/catalogo_ricette.json|" coordinates

CMD [ "python", "./botter.py" ]

