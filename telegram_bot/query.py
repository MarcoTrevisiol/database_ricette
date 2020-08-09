import json
import datetime
import isodate
import locale

locale.setlocale(locale.LC_TIME, "it_IT.utf8")
catalogo_file = '../catalogo_ricette.json'


def query_globali(chiave='titolo'):
    # funziona con 'id', 'titolo', 'portata', 'valutazione'
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    return set([r.get(chiave, '') for r in catalogo])


def query_categorie():
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    categorie = []
    for r in catalogo:
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


def query_ricette(**kwargs):
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    def do_pass_filter(r):
        if 'portata' in kwargs.keys():
            if not kwargs['portata'] == r.get('portata'):
                return False
        if 'categoria' in kwargs.keys():
            if not kwargs['categoria'] in r.get('categorie', []):
                return False
        if 'titolo' in kwargs.keys():
            if not kwargs['titolo'].lower() in r.get('titolo').lower():
                return False
        if 'ingrediente' in kwargs.keys():
            ingredienti = []
            for p in r.get('parti', []):
                ingredienti += [i.get('nome', '').lower() for i in p.get('ingredienti', [])
                                if i.get('principale') is True]
            if not kwargs['ingrediente'].lower() in ingredienti:
                return False
        if 'tempo' in kwargs.keys():
            if not datetime.timedelta(minutes=kwargs['tempo']) >= isodate.parse_duration(r.get('tempo', 'PT0M')):
                return False
        return True

    return [(r.get('id', '###'), r.get('titolo', '')) for r in catalogo if do_pass_filter(r)]


def query_by_id(id):
    with open(catalogo_file) as c_file:
        catalogo = json.load(c_file)

    ricetta = [r for r in catalogo if r.get('id', '###') == id]
    if len(ricetta) > 1:
        raise KeyError('Id collision on {}'.format(catalogo_file))

    return next(iter(ricetta), None)


def query_mese(mese=datetime.date.today().strftime('%b')):
    # TODO: as decorator
    pass