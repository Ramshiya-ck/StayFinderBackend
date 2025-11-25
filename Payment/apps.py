from django.apps import AppConfig
from django.conf import settings
import stripe


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Payment'


    def ready(self):
        # set the API key once at startup
        stripe.api_key = settings.STRIPE_SECRET_KEY
