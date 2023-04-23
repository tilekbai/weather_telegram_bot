from django.http import request
from pyowm import OWM
from weather_telegram_bot.settings import TOKEN_BOT, TOKEN_OWM
from django.core.management.commands.runserver import Command as RunServerCommand
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, MessageFilter
import logging
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()

list_get_coord = []
list_result = []

class FilterFloat(MessageFilter):
    def filter(self, message):
        try:
            float(message.text)
            if -90 < float(message.text) < 90:
                return float(message.text)
        except:
            pass


filter_float = FilterFloat()
def get_weather(request):
    global list_result
    owm = OWM(TOKEN_OWM)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_coords(lat=list_get_coord[0], lon=list_get_coord[1])
    w = observation.weather

    wind_speed = list_result.append(w.wind()["speed"])
    humidity = list_result.append(w.humidity)
    temperature = list_result.append(w.temperature("celsius")["temp"])
    cloudiness = list_result.append(w.clouds)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Узнайте погоду!")
    update.message.reply_text("Введите широту")

def echo(update: Update, context: CallbackContext):
    global list_get_coord
    global list_result
    list_get_coord.append(float(update.message.text))
    if len(list_get_coord) < 2:
        update.message.reply_text("Введите долготу")
    else:
        pass

    if len(list_get_coord) == 2:
        get_weather(request)
    if len(list_result) == 4:
        temperature = "Температура воздуха: " + str(round(list_result[2])) + " °C"
        humidity = "Влажность воздуха: " + str(list_result[1]) + "%"
        wind = "Скорость ветра: " + str(list_result[0]) + "м/c"
        cloudness = "Облачность: " + str(list_result[3]) + "%"
        update.message.reply_text("Погода по заданным координатам")
        update.message.reply_text(temperature)
        update.message.reply_text(humidity)
        update.message.reply_text(wind)
        update.message.reply_text(cloudness)
        list_result = []
        list_get_coord = []

def error(update: Update, context: CallbackContext):
    update.message.reply_text('An error occurred.')

def main():
    updater = Updater(TOKEN_BOT, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filter_float, echo))

    updater.start_polling()
    updater.idle()

class Command(RunServerCommand):
    def handle(self, *args, **options):
        main()
        super().handle(*args, **options)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)