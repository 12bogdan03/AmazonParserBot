import time
import os
import threading
import datetime

import schedule
from telegram import Bot, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

from scrapper import Scrapper
from models import User, Item
from database import session
import config

bot = Bot(config.TELEGRAM_TOKEN)


def run_threaded(job_func, args=None):
    if args is None:
        job_thread = threading.Thread(target=job_func)
    else:
        job_thread = threading.Thread(target=job_func, args=args)
    job_thread.start()


def start_schedule():
    while True:
        try:
            schedule.run_pending()
            time.sleep(3)
        except Exception as e:
            config.logger.exception(e)


def check_prices():
    users = session.query(User).all()
    scrapper = Scrapper()
    items = session.query(Item).all()
    for item in items:
        scrapper.go_to(item.link)
        price = scrapper.get_price()
        title = scrapper.get_title()
        if item.price:
            change_percentage = (abs(price - item.price) / item.price) * 100.0
            if change_percentage >= 3:
                item.price = price
                session.commit()
                markup = InlineKeyboardMarkup([InlineKeyboardButton('Check', url=item.link)])
                for u in users:
                    try:
                        bot.send_message(u.tg_id, '<code>{}</code> price changed'.format(title),
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=markup)
                    except Exception as e:
                        config.logger.error('Error sending a message: {}'.format(e))
        else:
            item.price = price
            session.commit()
