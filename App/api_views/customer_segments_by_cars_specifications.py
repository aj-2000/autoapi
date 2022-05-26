import pandas as pd
from django.http import HttpResponse, JsonResponse
from ..datasets.datasets import CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH, MPG_DATASET_ABSOLUTE_PATH, CARS_DATA_ABSOLUTE_PATH, SALES_DATASET_ABSOLUTE_PATH


def customer_segments_by_cars_specifications(request, option):
    if request.method == 'GET':
        if(option == 0):
            df = pd.read_csv(CARS_DATA_ABSOLUTE_PATH)
            df = df.groupby(['Drivetrain'])['Model'].count()
            df = (100. * df / df.sum()).round(1)
            jsonData = df.to_json(orient="columns")
        elif(option == 1):
            df = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
            df = df.groupby(['Transmission'])['Name'].count()
            df = (100. * df / df.sum()).round(1)
            jsonData = df.to_json(orient="columns")
        elif(option == 2):
            df = pd.read_csv(CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH)
            df.rename(columns={'Unnamed: 0': 'Brand', 'Unnamed: 1': 'Segment',
                               }, inplace=True)
            df = df.drop(labels=[0], axis=0, index=None, columns=None,
                         level=None, inplace=False, errors='raise')
            df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric)
            df['Sales'] = df.iloc[:, 0:].sum(axis=1)
            df = df.groupby(by='Segment')['Sales'].sum()
            df = (100. * df / df.sum()).round(1)
            jsonData = df.to_json(orient="columns")
        elif(option == 3):
            df = pd.read_csv(SALES_DATASET_ABSOLUTE_PATH)
            df['Sales'] = df.iloc[:, 3:].sum(axis=1)
            df = df.groupby(by='Brand')['Sales'].sum()
            df = df.astype('int32')
            jsonData = df.head(8).to_json(orient="columns")
        elif(option == 4):
            df = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
            df = df.groupby(['Fuel_Type'])['Name'].count()
            df = (100. * df / df.sum()).round(1)
            jsonData = df.to_json(orient="columns")
        elif(option == 5):
            df = pd.read_csv(CARS_DATA_ABSOLUTE_PATH)
            df = df.groupby(by="Body_Type")['Unnamed: 0'].count(
            ).sort_values(ascending=False)[0:9]
            df = (100. * df / df.sum()).round(1)
            jsonData = df.to_json(orient="columns")
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
