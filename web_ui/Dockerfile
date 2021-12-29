FROM httpd:latest

COPY . /usr/local/apache2/ricettario/
RUN rm htdocs/* ricettario/apache.conf && \
    ln -s ../ricettario htdocs/ricettario && \
    ln -s /var/local/database/catalogo_ricette.json ricettario/database
COPY ./apache.conf /usr/local/apache2/conf/httpd.conf
