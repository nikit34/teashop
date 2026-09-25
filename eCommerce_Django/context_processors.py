from django.conf import settings
from django.utils import timezone


def store(request):
    return {
        'STORE_NAME': getattr(settings, 'STORE_NAME', 'Portuguese Pantry'),
        'STORE_TAGLINE': getattr(settings, 'STORE_TAGLINE', ''),
        'STORE_YEAR': timezone.now().year,
    }
