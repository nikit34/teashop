from django.conf import settings
from django.utils import timezone


def store(request):
    return {
        'STORE_NAME': getattr(settings, 'STORE_NAME', 'Portuguese Pantry'),
        'STORE_TAGLINE': getattr(settings, 'STORE_TAGLINE', ''),
        'STORE_YEAR': timezone.now().year,
        'PRELAUNCH': getattr(settings, 'PRELAUNCH', False),
        'SELLER': {
            'name': getattr(settings, 'SELLER_NAME', ''),
            'nif': getattr(settings, 'SELLER_NIF', ''),
            'address': getattr(settings, 'SELLER_ADDRESS', ''),
            'email': getattr(settings, 'SELLER_EMAIL', ''),
            'phone': getattr(settings, 'SELLER_PHONE', ''),
            'vat_exempt': getattr(settings, 'SELLER_VAT_EXEMPT', False),
        },
    }
