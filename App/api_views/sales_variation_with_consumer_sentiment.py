import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import TOTAL_CAR_SALES_ABSOLUTE_PATH


def sales_variation_with_consumer_sentiment(request):
    if request.method == 'GET':
        df = pd.read_csv(TOTAL_CAR_SALES_ABSOLUTE_PATH)
        jsonData = df.to_json(orient="columns")
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
