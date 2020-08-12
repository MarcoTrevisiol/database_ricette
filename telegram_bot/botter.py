import logging
import logging.config
import configparser
import importlib.util
import json
import telegram.ext as te
import telegram as tele
import Levenshtein

conf_filename = "coordinates"
configuration = configparser.ConfigParser()
configuration.read(conf_filename)

logging.config.fileConfig(configuration['filenames']['logconf'])

query_module_name = 'query_catalogo'
query_module_filepath = 'query.py'
spec = importlib.util.spec_from_file_location(query_module_name, query_module_filepath)
query_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query_module)


def stringify_ingrediente(ingrediente, dosi):
    valore = ingrediente.get('quantita', {}).get('valore', 0) * dosi

    if valore == int(valore):
        valore = int(valore)

    template = "{v}{u} {nome}"
    if valore in (0, 1):
        if ingrediente.get('quantita', {}).get('unita', '') == '':
            template = "{nome}"
        else:
            template = "{u} {nome}"
    elif valore is float:
        template = "{v:04.2f}{u} {nome}"

    if ingrediente.get('annotazioni', '') != '':
        template += " ({ann})"

    return template.format(v=valore,
                          u=ingrediente.get('quantita', {}).get('unita', ''),
                          nome=ingrediente.get('nome', ''),
                          ann=ingrediente.get('annotazioni', ''))


def stringify_ingredienti(lista, dosi):
    return '\n'.join(["- {}".format(stringify_ingrediente(i, dosi)) for i in lista])


def stringify_variante(variante, dosi):
    text_variante = "Variante\n"
    if len(variante.get('ingredienti', [])) > 0:
        text_ingredienti = "<i>Ingredienti:</i>\n{}\n".format(
            stringify_ingredienti(variante.get('ingredienti', []), dosi)
        )
        text_variante += text_ingredienti
    if len(variante.get('procedura', '')) > 1:
        text_procedura = "<i>Procedura:</i>\n{}\n".format(variante.get('procedura'))
        text_variante += text_procedura
    return text_variante


def stringify_parte(parte, dosi, con_nome=False):
    text_ingredienti = "<i>Ingredienti:</i>\n{}\n".format(stringify_ingredienti(parte.get('ingredienti', []), dosi))
    if len(parte.get('procedura', '')) > 0:
        text_procedura = "<i>Procedura:</i>\n{}\n".format(parte.get('procedura'))
    else:
        text_procedura = ''
    text_varianti = '\n'.join([stringify_variante(v, dosi) for v in parte.get('varianti')])

    if con_nome:
        return "<b>per {}</b>:\n{}{}\n{}".format(parte.get('nome', 'questa parte'),
                                              text_ingredienti, text_procedura, text_varianti)
    else:
        return "{}{}\n{}".format(text_ingredienti, text_procedura, text_varianti)


def stringify_parti(parti, dosi):
    if len(parti) == 0:
        return ''
    elif len(parti) == 1:
        return stringify_parte(parti[0], dosi)
    else:
        return '\n'.join([stringify_parte(p, dosi, True) for p in parti])


def stringify_ricetta(ricetta, dosi=1):
    text_titolo = ricetta.get('titolo', 'Titolo')
    text_corpo = stringify_parti(ricetta.get('parti', []), dosi)
    fonte = ricetta.get('fonte', '')
    if fonte == '':
        text_fonte = ''
    else:
        text_fonte = '\n  Fonte: {}'.format(fonte)

    return "<b>{}</b>:\n{}{}".format(text_titolo, text_corpo, text_fonte)


def get_close_match(token, dictionary):
    termine = min(dictionary, key=lambda x: Levenshtein.distance(x.lower(), token.lower()))
    distance = Levenshtein.distance(termine.lower(), token.lower())
    logging.debug("{} è la migliore approssimazione di {}, dista {}".format(termine, token, distance))
    return distance


soglia = 2


def detect_query_type(token):
    checks = [
        ('portata', query_module.query_globali(chiave='portata')),
        ('categoria', query_module.query_categorie()),
        ('ingrediente', query_module.query_ingredienti()),
    ]
    for ch in checks:
        distance = get_close_match(token, ch[1])
        if distance < soglia:
            return ch[0]

    if token is not None:
        return 'titolo'
    raise KeyError


def build_query_kwargs(tokens):
    query_kwargs = {}
    for token in tokens:
        if Levenshtein.distance(token, 'tutti') < soglia:
            return {}

        query_type = detect_query_type(token)
        query_kwargs[query_type] = token
        logging.info("token \"{}\" interpretato come {}".format(token, query_type))
    return query_kwargs


def query_answer(lista_ricette):
    if len(lista_ricette) == 0:
        text_message = "Nessuna ricetta soddisfa i parametri di ricerca inseriti."
    else:
        text_lista = '\n'.join(["/id{} {} ({})".format(*r_pair) for r_pair in lista_ricette])
        text_message = "Ecco le ricette che ho trovato:\n{}".format(text_lista)
    return text_message


def start_callback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="<i>Fornisco ricette</i>")


text_help = """
<i>Fornisco ricette</i>
per trovare ricette, scrivi i termini di ricerca separati da ','
/categorie fornisce un elenco delle categorie disponibili
/dosi permette di visualizzare e modificare il dosaggio di default
"""


def help_callback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_help)
    logging.info('help requested')


def id_callback(update, context):
    command = update.effective_message.text.split(' ')[0]
    id_queried = command[3:]
    logging.info("{} -- {}".format(command, id_queried))

    if len(id_queried) < 5:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Id non inserito!")
        return

    recipe = query_module.query_by_id(id_queried)
    if recipe is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Id inesistente!")
        return

    dosi = context.chat_data.get('dosi', 0)
    if dosi == 0:
        context.chat_data['dosi'] = 4
        dosi = 4
    context.bot.send_message(chat_id=update.effective_chat.id, text=stringify_ricetta(recipe, dosi=dosi))


def dosi_callback(update, context):
    if len(context.args) < 1:
        dosi = context.chat_data.get('dosi', 0)
        if dosi == 0:
            context.chat_data['dosi'] = 4
            dosi = 4
        text_message = "Ricette tarate per {} dosi".format(dosi)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)
        return

    try:
        nuova_dose = int(context.args[0])
        context.chat_data['dosi'] = nuova_dose
        text_message = "Ricette tarate per {} dosi".format(nuova_dose)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)
    except ValueError:
        text_message = "Numero di dosi specificato non valido"
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)


def query_callback(update, context):
    query_kwargs = build_query_kwargs(update.effective_message.text.split(','))
    lista_ricette = query_module.query_ricette(**query_kwargs)

    if len(lista_ricette) == 0:
        logging.info("ricerca vuota: {}".format(query_kwargs))

    text_message = query_answer(lista_ricette)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)


def categorie_callback(update, context):
    set_portate = query_module.query_globali(chiave='portata')
    categorie = query_module.query_categorie() | set_portate

    try:
        categorie.remove('')
    except KeyError:
        pass

    keyboard_lista = []
    for i, cat in enumerate(sorted(list(categorie))):
        data = {'type': 'categoria', 'value': cat}
        if cat in set_portate:
            data['type'] = 'portata'
        data = json.dumps(data)
        if i % 2 == 0:
            keyboard_lista.append([tele.InlineKeyboardButton(cat, callback_data=data)])
        else:
            keyboard_lista[-1].append(tele.InlineKeyboardButton(cat, callback_data=data))

    text_message = "Ecco le categorie che ho trovato:"
    reply_markup = tele.InlineKeyboardMarkup(keyboard_lista)

    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message, reply_markup=reply_markup)


def categorie_button_callback(update, context):
    query = update.callback_query
    data = json.loads(query.data)
    query_kwargs = {data['type']: data['value']}
    lista_ricette = query_module.query_ricette(**query_kwargs)

    if len(lista_ricette) == 0:
        logging.info("ricerca vuota in risposta a /categorie ({})".format(query_kwargs))

    text_message = query_answer(lista_ricette)
    # CallbackQueries need to be answered, even if no notification to the user is needed
    query.answer()
    query.edit_message_text(text=text_message)


def error_callback(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "{}" caused error "{}"'.format(update, context.error))


def main_bot():
    persistence = te.PicklePersistence(filename=configuration["filenames"]["persistence"])
    defaults = te.Defaults(parse_mode=tele.ParseMode.HTML)
    with open(configuration["filenames"]["token"]) as token_file:
        token = token_file.read().strip()
    updater = te.Updater(token=token, use_context=True, persistence=persistence, defaults=defaults)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(te.CommandHandler("start", start_callback))
    dispatcher.add_handler(te.CommandHandler('help', help_callback))
    dispatcher.add_handler(te.CommandHandler('aiuto', help_callback))
    dispatcher.add_handler(te.MessageHandler(te.Filters.regex(r'^/id'), id_callback))
    dispatcher.add_handler(te.CommandHandler("dosi", dosi_callback))
    dispatcher.add_handler(te.CommandHandler("categorie", categorie_callback))
    dispatcher.add_handler(te.CallbackQueryHandler(categorie_button_callback))
    dispatcher.add_handler(te.MessageHandler(te.Filters.text, query_callback))
    dispatcher.add_error_handler(error_callback)

    updater.start_polling()
    updater.idle()


main_bot()
