import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import SALES_DATASET_ABSOLUTE_PATH


def top_five_best_and_worst_performers(request):
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
        sale["Percent Change"] = (
            (sale["2020 sales"] - sale["2019 sales"]) / sale["2019 sales"]) * 100
        decimals = 2
        sale['Percent Change'] = sale['Percent Change'].apply(
            lambda x: round(x, decimals))
        Top_5 = sale.nlargest(5, ['Percent Change'])
        Bottom_5 = sale.nsmallest(5, ['Percent Change'])
        frames = [Top_5, Bottom_5]
        top = pd.concat(frames)
        top = top.drop(['Total sales', '2020 sales', '2019 sales'], axis=1)
        jsonData = top.sort_values(
            by='Percent Change', ascending=True).to_json(orient='records')
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
