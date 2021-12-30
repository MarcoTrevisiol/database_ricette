#!/bin/sh

cd /var/local/database
date
git commit catalogo_ricette.json -m "Aggiornamento ricette"
git push backup master
