import logging
import configparser
import importlib.util
import telegram.ext as te

conf_filename = "coordinates"
configuration = configparser.ConfigParser()
configuration.read(conf_filename)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(configuration['filenames']['log']),
        logging.StreamHandler()
    ]
)

query_module_name = 'query_catalogo'
query_module_filepath = 'query.py'
spec = importlib.util.spec_from_file_location(query_module_name, query_module_filepath)
query_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query_module)


def stringify_ingrediente(ingrediente, dosi):
    template = "{v}{u} {nome}"
    valore = ingrediente.get('quantita', {}).get('valore', 0) * dosi
    if valore == int(valore):
        valore = int(valore)
    if valore is float:
        template = "{v:04.2f}{u} {nome}"
    return template.format(v=valore,
                          u=ingrediente.get('quantita', {}).get('unita', ''),
                          nome=ingrediente.get('nome', ''))


def stringify_ingredienti(lista, dosi):
    return '\n'.join(["- {}".format(stringify_ingrediente(i, dosi)) for i in lista])


def stringify_variante(variante, dosi):
    text_variante = "Variante\n"
    if len(variante.get('ingredienti', [])) > 0:
        text_ingredienti = "Ingredienti:\n{}\n".format(stringify_ingredienti(variante.get('ingredienti', []), dosi))
        text_variante += text_ingredienti
    if len(variante.get('procedura', '')) > 1:
        text_procedura = "Procedura:\n{}\n".format(variante.get('procedura'))
        text_variante += text_procedura
    return text_variante


def stringify_parte(parte, dosi, con_nome=False):
    text_ingredienti = "Ingredienti:\n{}\n".format(stringify_ingredienti(parte.get('ingredienti', []), dosi))
    if len(parte.get('procedura', '')) > 0:
        text_procedura = "Procedura:\n{}\n".format(parte.get('procedura'))
    else:
        text_procedura = ''
    text_varianti = '\n'.join([stringify_variante(v, dosi) for v in parte.get('varianti')])

    if con_nome:
        return "per {}:\n{}{}\n{}".format(parte.get('nome', 'questa parte'),
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

    return "{}:\n{}".format(text_titolo, text_corpo)


def start_callback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fornisco ricette")


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
    lista_ricette = query_module.query_ricette()
    text_lista = '\n'.join(["/id{} {}".format(*r_pair) for r_pair in lista_ricette])
    text_message = "Ricette presenti:\n{}".format(text_lista)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)


def main_bot():
    persistence = te.PicklePersistence(filename=configuration["filenames"]["persistence"])
    with open(configuration["filenames"]["token"]) as token_file:
        token = token_file.read().strip()
    updater = te.Updater(token=token, use_context=True, persistence=persistence)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(te.CommandHandler("start", start_callback))
    # dispatcher.add_handler(te.CommandHandler("id", id_callback))
    dispatcher.add_handler(te.MessageHandler(te.Filters.regex(r'^/id'), id_callback))
    dispatcher.add_handler(te.CommandHandler("dosi", dosi_callback))
    dispatcher.add_handler(te.MessageHandler(te.Filters.text, query_callback))


    updater.start_polling()
    updater.idle()


main_bot()
