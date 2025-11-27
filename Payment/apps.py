from django.apps import AppConfig
from django.conf import settings
import stripe


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Payment'

    def ready(self):
        # Set the Stripe API key once at startup (only if provided)
        # This is safe - no DB queries, no user creation, just configuration
        if settings.STRIPE_SECRET_KEY:
            stripe.api_key = settings.STRIPE_SECRET_KEY
