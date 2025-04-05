import configparser
import json
import re
import datetime
import locale
import logging

import levenshtein
import isodelta

conf_filename = "coordinates"
configuration = configparser.ConfigParser()
configuration.read(conf_filename)

locale.setlocale(locale.LC_TIME, "it_IT.utf8")
catalogo_file = configuration['filenames']['database']


def query_globali(chiave='titolo'):
    # funziona con 'id', 'titolo', 'portata', 'valutazione'
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    return set([r.get(chiave, '') for r in catalogo])


def query_categorie(with_portata=None):
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    categorie = []
    for r in catalogo:
        if with_portata is None or with_portata.lower() == r.get('portata', '').lower():
            categorie += r.get('categorie', [])
    return set(categorie)


def query_ingredienti(solo_principali=True, chiave='nome'):
    # funziona con 'nome', 'annotazione', 'unita'
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    def get_chiave(i):
        if chiave == 'unita':
            return i.get('quantita', {}).get('chiave', '')
        return i.get(chiave, '')

    ingredienti = []
    for r in catalogo:
        for p in r.get('parti', []):
            ingredienti += [get_chiave(i) for i in p.get('ingredienti', []) if
                            not solo_principali or i.get('principale') is True]
            for v in p.get('varianti', []):
                ingredienti += [get_chiave(i) for i in v.get('ingredienti', []) if
                                not solo_principali or i.get('principale') is True]
    return set(ingredienti)


def equal_enough(left_term, right_term):
    return levenshtein.distance(left_term, right_term) < int(configuration['default']['soglia'])


def belong_enough(term, dictionary):
    if len(dictionary) == 0:
        return False
    termine = min(dictionary, key=lambda x: levenshtein.distance(term, x))
    return levenshtein.distance(term, termine) < int(configuration['default']['soglia'])


def compute_duration(token):
    match = re.search(r"^([0-9]+)\s*([dgho'm])", token)
    amount = int(match.group(1))
    if match.group(2) in list("'m"):
        return amount
    if match.group(2) in list("ho"):
        return amount * 60
    if match.group(2) in list("dg"):
        return amount * 60 * 24
    return 0


def query_ricette(**kwargs):
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    def do_pass_filter(r):
        if 'periodo' not in kwargs.keys():
            if datetime.date.today().strftime('%b') not in r.get('periodo', []):
                return False
        if 'portata' in kwargs.keys():
            if not equal_enough(kwargs['portata'].lower(), r.get('portata', '').lower()):
                return False
        if 'categoria' in kwargs.keys():
            if not belong_enough(kwargs['categoria'].lower(),
                                 [cat.lower() for cat in r.get('categorie', [])]):
                return False
        if 'titolo' in kwargs.keys():
            if not kwargs['titolo'].lower() in r.get('titolo').lower():
                return False
        if 'ingrediente' in kwargs.keys():
            ingredienti = []
            for p in r.get('parti', []):
                ingredienti += [i.get('nome', '').lower() for i in p.get('ingredienti', [])
                                if i.get('principale') is True]
            if not belong_enough(kwargs['ingrediente'].lower(), ingredienti):
                return False
        if 'tempo' in kwargs.keys():
            if not datetime.timedelta(minutes=compute_duration(kwargs['tempo'])) >=\
                   isodelta.parse_duration(r.get('tempo', 'PT0M')):
                return False
        return True

    def stringify_duration(iso):
        duration = isodelta.parse_duration(iso)
        humanized = ''
        if duration.days > 0:
            humanized += '{}d'.format(duration.days)
        remaining = duration.seconds
        if remaining // 3600 > 0:
            humanized += '{}h'.format(remaining // 3600)
            remaining -= remaining // 3600 * 3600
        if remaining // 60 > 0:
            humanized += "{}'".format(remaining // 60)
        if humanized == '':
            humanized = "?"
        return humanized

    return [(r.get('id', '###'), r.get('titolo', ''), stringify_duration(r.get('tempo', 'PT0M')))
            for r in catalogo if do_pass_filter(r)]


def query_by_id(id_ricetta):
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    ricetta = [r for r in catalogo if r.get('id', '###') == id_ricetta]
    if len(ricetta) > 1:
        raise KeyError('Id collision on {}'.format(catalogo_file))

    return next(iter(ricetta), None)


def get_close_match(token, dictionary):
    termine = min(dictionary, key=lambda x: levenshtein.distance(x.lower(), token.lower()))
    distance = levenshtein.distance(termine.lower(), token.lower())
    logging.debug("{} è la migliore approssimazione di {}, dista {}"
                  .format(termine, token, distance))
    return distance


def detect_query_type(token):
    checks = [
        ('portata', query_globali(chiave='portata')),
        ('categoria', query_categorie()),
        ('ingrediente', query_ingredienti()),
    ]
    for ch in checks:
        distance = get_close_match(token, ch[1])
        if distance < int(configuration['default']['soglia']):
            return ch[0]

    match = re.search(r"^[0-9]+\s*[dgho'm]", token)
    if match is not None:
        return 'tempo'
    if token is not None:
        return 'titolo'
    raise KeyError


def build_query_kwargs(tokens):
    query_kwargs = {}
    for token in tokens:
        token = token.strip()
        if levenshtein.distance(token, 'tutti') < int(configuration['default']['soglia']):
            return {}

        query_type = detect_query_type(token)
        query_kwargs[query_type] = token
        logging.info("token \"{}\" interpretato come {}".format(token, query_type))
    return query_kwargs


def query_answer(lista_ricette, stagionalita=True):
    if len(lista_ricette) == 0:
        if stagionalita:
            text_message = "Nessuna ricetta di stagione soddisfa i parametri di ricerca inseriti."
        else:
            text_message = "Nessuna ricetta soddisfa i parametri di ricerca inseriti."
    else:
        text_lista = '\n'.join(["{1} ({2}) /id{0}".format(*r_pair)
                                for r_pair in sorted(lista_ricette, key=lambda x: x[1])])
        text_message = "Ecco le ricette che ho trovato:\n{}".format(text_lista)
    return text_message
