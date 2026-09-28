import re

SOURCE_RE = re.compile(r'^[a-z0-9][a-z0-9_-]{0,39}$')


class SourceTagMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        source = request.GET.get('src', '').strip().lower()
        if source and SOURCE_RE.match(source):
            request.session['src'] = source
        return self.get_response(request)
