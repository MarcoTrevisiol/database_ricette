FROM debian:stable-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apache2 python3 libapache2-mod-wsgi-py3

WORKDIR /var/www
COPY ./apache.conf /etc/apache2/sites-available/site.conf
COPY . /usr/local/ricettario/
RUN a2dissite 000-default.conf && \
    a2ensite site.conf && \
    a2enmod rewrite && \
    rm -r * && \
    ln -s /usr/local/ricettario . && \
    ln -s /var/local/database/catalogo_ricette.json /usr/local/ricettario/database

ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
