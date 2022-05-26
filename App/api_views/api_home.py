from django.http import HttpResponse


def api_home(request):
    if request.method:
        html = "<html><body>API Working Fine</body></html>"
        return HttpResponse(html)
