FROM debian:stable-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron

WORKDIR /usr/local/
COPY backup-cron ./
COPY backup.sh ./
RUN chmod 0644 backup-cron && \
    chmod 0700 backup.sh && \
    crontab backup-cron

CMD ["cron", "-f"]
