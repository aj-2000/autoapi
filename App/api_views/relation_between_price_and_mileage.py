import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import MPG_DATASET_ABSOLUTE_PATH

# Relation between Price and Mileage


def relation_between_price_and_mileage(request, option):
    if request.method == 'GET':
        autoMPG = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
        if option == 1:
            jsonData = autoMPG[autoMPG['Transmission'] == 'Automatic'][[
                'Price', 'Mileage Km/L']].head(200).to_json(orient='columns')
        elif option == 2:
            jsonData = autoMPG[autoMPG['Transmission'] == 'Manual'][[
                'Price', 'Mileage Km/L']].head(200).to_json(orient='columns')
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
