import configparser
import json
import logging
import logging.config
import os
import re

import telegram as tele
import telegram.ext as te

import stringify
import query as query_module
import levenshtein

conf_filename = "coordinates"
configuration = configparser.ConfigParser()
configuration.read(conf_filename)

logging.config.fileConfig(configuration['filenames']['logconf'])


def get_close_match(token, dictionary):
    termine = min(dictionary, key=lambda x: levenshtein.distance(x.lower(), token.lower()))
    distance = levenshtein.distance(termine.lower(), token.lower())
    logging.debug("{} è la migliore approssimazione di {}, dista {}"
                  .format(termine, token, distance))
    return distance


def detect_query_type(token):
    checks = [
        ('portata', query_module.query_globali(chiave='portata')),
        ('categoria', query_module.query_categorie()),
        ('ingrediente', query_module.query_ingredienti()),
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


def logg_stringify_update(update):
    try:
        segno = "|Chat:{}|Message:'text'='{}';'callback_query'='{}';'date'='{}'|".format(
            update.effective_chat,
            update.effective_message.text,
            update.callback_query.data,
            update.effective_message.date
        )
    except AttributeError:
        segno = "|Chat:{}|Message:'text'='{}';'date'='{}'|".format(
            update.effective_chat,
            update.effective_message.text,
            update.effective_message.date
        )
    return segno


async def start_callback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="<i>Fornisco ricette</i>")
    logging.info("start with update={}".format(logg_stringify_update(update)))


async def help_callback(update, context):
    text_help = configuration['help']['message'].replace('\\n', '\n')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_help)
    logging.info("help with update={}".format(logg_stringify_update(update)))


async def id_callback(update, context):
    command = update.effective_message.text.split(' ')[0]
    id_queried = command[3:]
    logging.info("id with update={}".format(logg_stringify_update(update)))

    if len(id_queried) < 5:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Id non inserito!")
        return

    recipe = query_module.query_by_id(id_queried)
    if recipe is None:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Id inesistente!")
        return

    dosi = context.chat_data.get('dosi', 0)
    if dosi == 0:
        context.chat_data['dosi'] = 4
        dosi = 4
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=stringify.ricetta(recipe, dosi=dosi))


async def dosi_callback(update, context):
    logging.info("dosi with update={}".format(logg_stringify_update(update)))
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


async def stagione_callback(update, context):
    logging.info("stagione with update={}".format(logg_stringify_update(update)))
    stagionalita_attuale = context.chat_data.get('stagione', True)
    context.chat_data['stagione'] = not stagionalita_attuale
    if stagionalita_attuale:
        text_message = "Ora vengono mostrate tutte le ricette, anche quelle non di stagione"
    else:
        text_message = "Ora vengono mostrate solo le ricette di stagione"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)


async def query_callback(update, context):
    logging.info("query with update={}".format(logg_stringify_update(update)))
    query_kwargs = build_query_kwargs(update.effective_message.text.split(','))
    if not context.chat_data.get('stagione', True):
        query_kwargs['periodo'] = True
    lista_ricette = query_module.query_ricette(**query_kwargs)

    if len(lista_ricette) == 0:
        logging.info("ricerca vuota: {}".format(query_kwargs))

    text_message = query_answer(lista_ricette,
                                stagionalita=context.chat_data.get('stagione', True))
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)


async def categorie_callback(update, context):
    logging.info("categorie with update={}".format(logg_stringify_update(update)))
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

    text_message = "<i>Ecco le categorie che ho trovato:</i>"
    reply_markup = tele.InlineKeyboardMarkup(keyboard_lista)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text_message, reply_markup=reply_markup)


async def categorie_button_callback(update, context):
    query = update.callback_query
    data = json.loads(query.data)
    query_kwargs = {data['type']: data['value']}
    if not context.chat_data.get('stagione', True):
        query_kwargs['periodo'] = True
    lista_ricette = query_module.query_ricette(**query_kwargs)

    if len(lista_ricette) == 0:
        logging.warning("ricerca vuota in risposta a /categorie ({})".format(query_kwargs))

    text_message = query_answer(lista_ricette,
                                stagionalita=context.chat_data.get('stagione', True))
    # CallbackQueries need to be answered, even if no notification to the user is needed
    query.answer()
    query.edit_message_text(text=text_message)


async def portate_callback(update, context):
    logging.info("portate with update={}".format(logg_stringify_update(update)))
    set_portate = sorted(list(query_module.query_globali(chiave='portata')))

    try:
        set_portate.remove('')
    except (KeyError, ValueError):
        pass

    keyboard_lista = [[tele.InlineKeyboardButton(por, callback_data=json.dumps({'portata': por, 'S': True}))]
                      for por in sorted((list(set_portate)))]

    text_message = "<i>Ecco le portate che ho trovato:</i>"
    reply_markup = tele.InlineKeyboardMarkup(keyboard_lista)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text_message, reply_markup=reply_markup)


async def keyboard_portata_callback(update, context, data):
    categorie = query_module.query_categorie(with_portata=data['portata'])
    try:
        categorie.remove('')
    except (KeyError, ValueError):
        pass

    keyboard_lista = [[tele.InlineKeyboardButton(cat, callback_data=
    json.dumps({'portata': data['portata'], 'categoria': cat, 'S': False}))]
                      for cat in sorted(list(categorie))]
    keyboard_lista.append([tele.InlineKeyboardButton('Tutte', callback_data=
    json.dumps({'portata': data['portata'], 'S': False}))])

    text_message = "<i>Ecco le categorie che ho trovato:</i>"
    reply_markup = tele.InlineKeyboardMarkup(keyboard_lista)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text_message, reply_markup=reply_markup)


async def portate_button_callback(update, context):
    logging.info("portate button with update={}".format(logg_stringify_update(update)))
    query = update.callback_query
    data = json.loads(query.data)
    if 'S' not in data.keys():
        return categorie_button_callback(update, context)

    if data['S']:
        return keyboard_portata_callback(update, context, data)

    if not context.chat_data.get('stagione', True):
        data['periodo'] = True
    lista_ricette = query_module.query_ricette(**data)

    if len(lista_ricette) == 0:
        logging.info("ricerca vuota in risposta a /categorie ({})".format(data))

    text_message = query_answer(lista_ricette,
                                stagionalita=context.chat_data.get('stagione', True))
    # CallbackQueries need to be answered, even if no notification to the user is needed
    query.answer()
    query.edit_message_text(text=text_message)


async def error_callback(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "{}" Error "{}"'.format(update, context.error))


def get_secret_token():
    try:
        with open(configuration["filenames"]["token"]) as token_file:
            token = token_file.read().strip()
    except FileNotFoundError:
        token = os.getenv('TOKEN')
    if not token:
        raise TypeError("Secret Telegram Token not found!")
    return token


def main_bot():
    persistence = te.PicklePersistence(filepath=configuration["filenames"]["persistence"])
    defaults = te.Defaults(parse_mode=tele.constants.ParseMode.HTML)
    token = get_secret_token()
    application = (te.Application.builder()
                   .token(token)
                   .defaults(defaults)
                   .persistence(persistence)
                   .context_types(te.ContextTypes())
                   .build())

    application.add_handler(te.CommandHandler("start", start_callback))
    application.add_handler(te.CommandHandler("help", help_callback))
    application.add_handler(te.CommandHandler("aiuto", help_callback))
    application.add_handler(te.MessageHandler(te.filters.Regex(r'^/id'), id_callback))
    application.add_handler(te.CommandHandler("dosi", dosi_callback))
    application.add_handler(te.CommandHandler("stagione", stagione_callback))
    application.add_handler(te.CommandHandler("categorie", categorie_callback))
    application.add_handler(te.CommandHandler("portate", portate_callback))
    application.add_handler(te.CallbackQueryHandler(portate_button_callback))
    application.add_handler(te.MessageHandler(te.filters.Text(), query_callback))
    application.add_error_handler(error_callback)

    application.run_polling(allowed_updates=tele.Update.ALL_TYPES)


main_bot()
