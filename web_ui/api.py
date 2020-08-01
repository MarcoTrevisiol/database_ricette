import os
import json
import string
import random

template_location = "templates/"
template_error = "{}error.html".format(template_location)


def ciao(*args, **kwargs):
    print(os.getcwd())
    ciao_filename = "{}ciao.html".format(template_location)
    with open(ciao_filename) as file:
        return file.read()


def errore(*args, **kwargs):
    messaggio = kwargs.get('messaggio', "Siamo fregati!")
    with open(template_error) as file:
        return file.read().format(descrizione=messaggio)


def nuova_ricetta(*args, **kwargs):
    # Ricevo il corpo della richiesta di nuova ricetta
    corpo = kwargs.get('corpo', '')
    # controllo che sia json
    try:
        j_corpo = json.loads(corpo)
    except json.JSONDecodeError:
        return errore(messaggio='json mal formato')

    # controllo che ci sia un titolo
    try:
        assert len(j_corpo['titolo']) > 0
    except (KeyError, AssertionError):
        return errore(messaggio='titolo della ricetta mancante')

    # controllo che ci sia almeno un ingrediente principale
    try:
        ingredienti = []
        for parte in j_corpo['parti']:
            ingredienti += [i for i in parte['ingredienti'] if 'principale' in i and i['principale']]
        assert len(ingredienti) > 0
    except (KeyError, AssertionError):
        return errore(messaggio='nessun ingrediente principale inserito')

    # genero un id probabilmente unico
    alphabet = string.ascii_lowercase + string.digits
    j_corpo['id'] = ''.join(random.choices(alphabet, k=8))

    # salvo la nuova ricetta nel database
    database_filename = '../catalogo_ricette.json'
    with open(database_filename) as db_ricette:
        elenco_ricette = json.load(db_ricette)
    elenco_ricette.append(j_corpo)
    with open(database_filename, 'w') as db_ricette:
        json.dump(elenco_ricette, db_ricette)

    with open('{}ok.html'.format(template_location)) as html_file:
        return html_file.read()
