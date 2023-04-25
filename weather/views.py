import telegram
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from weather_telegram_bot.settings import TOKEN_BOT


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telegram.Update.de_json(json.loads(request.body), bot)
        print(update)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

bot = telegram.Bot(token=TOKEN_BOT)
# Create your views here.
