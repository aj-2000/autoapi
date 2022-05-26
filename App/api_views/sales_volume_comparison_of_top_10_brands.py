import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import SALES_DATASET_ABSOLUTE_PATH


def sales_volume_comparison_of_top_10_brands(request):
    if request.method == 'GET':
        sale = pd.read_csv(SALES_DATASET_ABSOLUTE_PATH)
        sale['2019 sales'] = sale['Q1 2019'] + \
            sale['Q2 2019'] + sale['Q3 2019']
        sale['2020 sales'] = sale['Q1 2020'] + \
            sale['Q2 2020'] + sale['Q3 2020']
        drop_col = ['Avg Price', 'Q1 2019', 'Q2 2019', 'Q3 2019', 'Q4 2019', 'Q1 2020', 'Q2 2020', 'Q3 2020', 'Q4 2020',
                    'Autogroup']
        sale = sale.drop(drop_col, axis=1)
        sale['Total sales'] = sale['2019 sales'] + sale['2020 sales']
        sale = sale.sort_values(by='Total sales', axis=0, ascending=False)
        sale = sale.head(10)
        sale = sale.drop(['Total sales'], axis=1)
        jsonData = sale.to_json(orient='columns')
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
