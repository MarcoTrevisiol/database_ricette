import os
import json
import string
import random


def errore(*args, **kwargs):
    risposta = {
        'codice': 'errore',
        'messaggio': kwargs.get('messaggio', "Siamo fregati!"),
    }
    return json.dumps(risposta)


def nuova_ricetta(*args, **kwargs):
    # Ricevo il corpo della richiesta di nuova ricetta
    corpo = kwargs.get('corpo', '')
    # controllo che sia json
    try:
        j_corpo = json.loads(corpo)
    except (json.JSONDecodeError, TypeError):
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

    # tolgo il valore "dosi" portato dall'interfaccia angular
    try:
        del j_corpo['dosi']
    except KeyError:
        pass

    # salvo la nuova ricetta nel database
    database_filename = '../catalogo_ricette.json'
    with open(database_filename) as db_ricette:
        elenco_ricette = json.load(db_ricette)
    elenco_ricette.append(j_corpo)
    with open(database_filename, 'w') as db_ricette:
        json.dump(elenco_ricette, db_ricette)

    risposta = {
        'codice': 'ok',
        'messaggio': "Nuova ricetta registrata correttamente",
        'id': j_corpo['id'],
    }
    return json.dumps(risposta)


def lista_ricette(*args, **kwargs):
    database_filename = '../catalogo_ricette.json'
    with open(database_filename) as c_file:
        catalogo = json.load(c_file)

    lista_titoli = [(r.get('id', '###'), r.get('titolo', '')) for r in catalogo]
    return json.dumps(lista_titoli)


def ottieni_ricetta(*args, **kwargs):
    database_filename = '../catalogo_ricette.json'
    with open(database_filename) as c_file:
        catalogo = json.load(c_file)

    id = kwargs.get('query', '####')
    ricetta = [r for r in catalogo if r.get('id', '###') == id]

    if len(ricetta) > 1:
        raise KeyError('Id collision on {}'.format(database_filename))

    if len(ricetta) == 0:
        return '{}'

    return json.dumps(ricetta[0])


def update_ricetta(*args, **kwargs):
    # Ricevo il corpo della richiesta di nuova ricetta
    corpo = kwargs.get('corpo', '')
    # controllo che sia json
    try:
        j_corpo = json.loads(corpo)
    except (json.JSONDecodeError, TypeError):
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

    # controllo che l'id esista
    try:
        id = kwargs['query']
        assert id == j_corpo['id']
    except (KeyError, AssertionError):
        return errore(messaggio='id non valido o non specificato')

    # tolgo il valore "dosi" portato dall'interfaccia angular
    try:
        del j_corpo['dosi']
    except KeyError:
        pass

    # rimpiazzo la ricetta
    database_filename = '../catalogo_ricette.json'
    with open(database_filename) as db_ricette:
        elenco_ricette = json.load(db_ricette)
    index_to_replace = next(i for i, v in enumerate(elenco_ricette) if v['id'] == id)
    elenco_ricette[index_to_replace] = j_corpo
    with open(database_filename, 'w') as db_ricette:
        json.dump(elenco_ricette, db_ricette)

    risposta = {
        'codice': 'ok',
        'messaggio': "Ricetta modificata correttamente",
    }
    return json.dumps(risposta)
