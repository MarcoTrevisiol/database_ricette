import math


def quantita(valore):
    if valore == int(valore) and valore < 10:
        return str(int(valore))

    esponente = math.floor(math.log10(valore)) - 1
    valore_arrotondato = round(valore / 10 ** esponente) * 10 ** esponente

    if valore_arrotondato >= 10:
        return str(valore_arrotondato)
    return "{:.2g}".format(valore_arrotondato).replace('.', ',')


def ingrediente(item, dosi):
    valore = item.get('quantita', {}).get('valore', 0) * dosi

    if valore in (0, 1):
        template = "{u} {nome}"
    else:
        template = "{v}{u} {nome}"
    if item.get('annotazioni', '') != '':
        template += " ({ann})"

    return template.format(v=quantita(valore),
                           u=item.get('quantita', {}).get('unita', ''),
                           nome=item.get('nome', ''),
                           ann=item.get('annotazioni', ''))


def ingredienti(lista, dosi):
    return '\n'.join(["- {}".format(ingrediente(i, dosi)) for i in lista])


def variante(item, dosi):
    text_variante = "Variante\n"
    if len(item.get('ingredienti', [])) > 0:
        text_ingredienti = "<i>Ingredienti:</i>\n{}\n".format(
            ingredienti(item.get('ingredienti', []), dosi)
        )
        text_variante += text_ingredienti
    if len(item.get('procedura', '')) > 1:
        text_procedura = "<i>Procedura:</i>\n{}\n".format(item.get('procedura'))
        text_variante += text_procedura
    return text_variante


def parte(item, dosi, con_nome=False):
    text_ingredienti = "<i>Ingredienti:</i>\n{}\n".format(ingredienti(
        item.get('ingredienti', []), dosi))
    if len(item.get('procedura', '')) > 0:
        text_procedura = "<i>Procedura:</i>\n{}\n".format(item.get('procedura'))
    else:
        text_procedura = ''
    text_varianti = '\n'.join([variante(v, dosi) for v in item.get('varianti')])

    if con_nome:
        return "<b>per {}</b>:\n{}{}\n{}".format(item.get('nome', 'questa parte'),
                                                 text_ingredienti, text_procedura, text_varianti)
    else:
        return "{}{}\n{}".format(text_ingredienti, text_procedura, text_varianti)


def parti(items, dosi):
    if len(items) == 0:
        return ''
    elif len(items) == 1:
        return parte(items[0], dosi)
    else:
        return '\n'.join([parte(p, dosi, True) for p in items])


def ricetta(item, dosi=1):
    text_titolo = item.get('titolo', 'Titolo')
    text_corpo = parti(item.get('parti', []), dosi)
    fonte = item.get('fonte', '')
    if fonte == '':
        text_fonte = ''
    else:
        text_fonte = '\n  <i>Fonte: {}</i>'.format(fonte)

    return "<b>{}</b>:\n{}{}".format(text_titolo, text_corpo, text_fonte)
