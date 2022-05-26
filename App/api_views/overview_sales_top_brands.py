import pandas as pd
import json
from django.http import HttpResponse, JsonResponse


from ..datasets.datasets import CARS_YEARLY_SALES_ABSOLUTE_PATH


def overview_sales_top_brands(request):
    if request.method == 'GET':
        df_sales = pd.read_csv(CARS_YEARLY_SALES_ABSOLUTE_PATH)
        dataDict = {
            'sales': df_sales.sum()[2:].to_json(),
            'top_brand_of_year': df_sales.sort_values(by='2022', ascending=False).head(1)['Make'].item(),
            'top_brand_of_month': df_sales.sort_values(by='June_2022', ascending=False).head(1)['Make'].item()
        }
        jsonData = json.dumps(dataDict)
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
