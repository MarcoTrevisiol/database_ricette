FROM debian:stable-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron git ca-certificates

WORKDIR /usr/local/
COPY backup-cron ./etc
COPY backup.sh ./bin
RUN chmod 0644 etc/backup-cron && \
    chmod 0700 bin/backup.sh && \
    git config --global user.email "marco.trevisiol@sns.it" && \
    git config --global user.name "MarcoTrevisiol" && \
    crontab etc/backup-cron && \
    touch /var/log/cron.log

CMD ["cron", "-f"]
