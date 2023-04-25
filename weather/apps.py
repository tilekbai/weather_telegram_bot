from django.apps import AppConfig
from weather.management.commands.bot import main

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    # def ready(self):
    #     main()

