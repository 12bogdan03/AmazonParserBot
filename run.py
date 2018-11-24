import schedule

from telegram_bot import updater
from thread_svc import start_schedule, run_threaded, check_prices

schedule.every(3).minutes.do(check_prices)
run_threaded(start_schedule)

updater.start_polling()
