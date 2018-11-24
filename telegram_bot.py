import uuid
import datetime
import os

from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CommandHandler, Updater, MessageHandler,
                          Filters, CallbackQueryHandler, ConversationHandler)

import config
from models import User, Item
from database import session
from telegram_svc import restricted, error_callback, build_menu, token_needed

updater = Updater(token=config.TELEGRAM_TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
    user = session.query(User).filter(
        User.tg_id == update.message.chat_id
    ).first()
    if not user:
        user = User(tg_id=update.message.chat_id)
        session.add(user)
        session.commit()

    update.message.reply_text("Hello, @{} "
                              "[<code>{}</code>]".format(update.message.from_user.username,
                                                         update.message.chat_id),
                              parse_mode=ParseMode.HTML)


def add_item(bot, update, args):
    if len(args) == 1:
        existing_item = session.query(Item).filter(
            Item.link == args[0]
        ).first()
        if existing_item:
            update.message.reply_text("This item is already being monitored.")
            return
        item = Item(link=args[0])
        session.add(item)
        session.commit()
        update.message.reply_text("<b>Great, item added!</b>",
                                  parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text("Please, send me the link like in the example:\n"
                                  "/add <code>[link]</code>",
                                  parse_mode=ParseMode.HTML)


def delete_item(bot, update, args):
    if len(args) == 1:
        item = session.query(Item).filter(
            Item.link == args[0]
        ).first()
        if item:
            session.delete(item)
            session.commit()
            update.message.reply_text("Item deleted from monitoring.")
        else:
            update.message.reply_text("No items found.")
    else:
        update.message.reply_text("Please, send me the link like in the example:\n"
                                  "/delete <code>[link]</code>",
                                  parse_mode=ParseMode.HTML)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('add', add_item, pass_args=True))
dispatcher.add_handler(CommandHandler('delete', delete_item, pass_args=True))
dispatcher.add_error_handler(error_callback)
