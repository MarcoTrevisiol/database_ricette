import json
import string
import random

database_filename = 'database'


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

    try:
        month_ordered = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic']
        j_corpo['periodo'] = [m for m in month_ordered if m in j_corpo['periodo']]
    except KeyError:
        pass

    # salvo la nuova ricetta nel database
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
    with open(database_filename) as c_file:
        catalogo = json.load(c_file)

    lista_titoli = [{
            'id': r.get('id', '###'),
            'titolo': r.get('titolo', ''),
            'tempo': r.get('tempo', 'PT0M'),
            'portata': r.get('portata', ''),
            'categorie': r.get('categorie', []),
            'fonte': r.get('fonte', '')
        }
        for r in catalogo]
    return json.dumps(lista_titoli)


def ottieni_ricetta(*args, **kwargs):
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

    try:
        month_ordered = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic']
        j_corpo['periodo'] = [m for m in month_ordered if m in j_corpo['periodo']]
    except KeyError:
        pass

    # rimpiazzo la ricetta
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


def lista_ingredienti(*args, **kwargs):
    with open(database_filename) as c_file:
        catalogo = json.load(c_file)

    ingredienti_totali = []
    for r in catalogo:
        for p in r.get('parti', []):
            ingredienti_totali += p.get('ingredienti', [])
            for v in p.get('varianti', []):
                ingredienti_totali += v.get('ingredienti', [])

    return json.dumps(list({i.get('nome', '') for i in ingredienti_totali}))
