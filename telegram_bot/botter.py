import logging
import configparser
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


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Fornisco ricette")


def main_bot():
    persistence = te.PicklePersistence(filename=configuration["filenames"]["persistence"])
    with open(configuration["filenames"]["token"]) as token_file:
        token = token_file.read().strip()
    updater = te.Updater(token=token, use_context=True, persistence=persistence)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(te.CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


main_bot()
