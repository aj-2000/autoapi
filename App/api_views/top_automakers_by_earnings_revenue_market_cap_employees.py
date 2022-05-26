import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import AUTOMAKERS_BY_EARNING_ABSOLUTE_PATH, AUTOMAKERS_BY_REVENUE_ABSOLUTE_PATH, AUTOMAKERS_BY_MARKET_CAPITALIZATION_ABSOLUTE_PATH, AUTOMAKERS_BY_EMPLOYEES_ABSOLUTE_PATH


def top_automakers_by_earnings_revenue_market_cap_employees(request, option):
    if request.method == 'GET':
        if(option == 0):
            df = pd.read_csv(AUTOMAKERS_BY_EARNING_ABSOLUTE_PATH)
            df['earnings_ttm'] = df['earnings_ttm']/1000000000
            df = df.iloc[0:10, [1, 3]]
        elif(option == 1):
            df = pd.read_csv(AUTOMAKERS_BY_REVENUE_ABSOLUTE_PATH)
            df['revenue_ttm'] = df['revenue_ttm']/1000000000
            df = df.iloc[0:10, [1, 3]]
        elif(option == 2):
            df = pd.read_csv(AUTOMAKERS_BY_MARKET_CAPITALIZATION_ABSOLUTE_PATH)
            df['marketcap'] = df['marketcap'] / 1000000000
            df = df.iloc[0:10, [1, 3]]
        elif(option == 3):
            df = pd.read_csv(AUTOMAKERS_BY_EMPLOYEES_ABSOLUTE_PATH)
            df = df.iloc[0:10, [1, 3]]
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        df = df.round()
        jsonData = df.to_json(orient="columns")
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
