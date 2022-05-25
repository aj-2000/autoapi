import pandas as pd
import json
import numpy as np
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
import os
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error,mean_absolute_percentage_error
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

dirname = os.path.dirname(__file__)
MPG_DATASET_ABSOLUTE_PATH = os.path.join(dirname, 'autoMPGFinal.csv')
SALES_DATASET_ABSOLUTE_PATH = os.path.join(dirname, 'Car_data.csv')
AUTO_MARKET_SHARE_DATA_ABSOLUTE_PATH = os.path.join(dirname, 'AutoMarketShare.csv')
CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH = os.path.join(dirname, 'Car sales by month.csv')
CARS_DATA_ABSOLUTE_PATH = os.path.join(dirname, 'autodata-cars.csv')
CARS_YEARLY_SALES_ABSOLUTE_PATH = os.path.join(dirname, 'car_sales_year.csv')
TOTAL_CAR_SALES_ABSOLUTE_PATH = os.path.join(dirname, 'Total_Car_Sales.csv')
PRODUCTION_OF_VEHICLES_DATA_ABSOLUTE_PATH = os.path.join(dirname, 'productionOfVehicles.csv')
TOP_COUNTRIES_DATA_ABSOLUTE_DATA = os.path.join(dirname, 'top_countries.csv')
AUTOMAKERS_BY_EARNING_ABSOLUTE_PATH = os.path.join(dirname, 'automakers_by_earning.csv')
AUTOMAKERS_BY_EMPLOYEES_ABSOLUTE_PATH = os.path.join(dirname, 'automakers_by_employees.csv')
AUTOMAKERS_BY_MARKET_CAPITALIZATION_ABSOLUTE_PATH = os.path.join(dirname, 'automakers_by_market_capitalization.csv')
AUTOMAKERS_BY_REVENUE_ABSOLUTE_PATH = os.path.join(dirname, 'automakers_by_revenue.csv')

# DF Test utility for Time series analyis

# Processed Data
# MPG_DATASET_PROCESSED_ABSOLUTE_PATH = os.path.join(dirname, 'autodata-mpg.csv')

# Relation between Price and Mileage
def queryOne(request, option):
    slug = option
    print(slug)
    if request.method == 'GET':
        autoMPG = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
        if option == 1:
            jsonData = autoMPG[autoMPG['Transmission']=='Automatic'][['Price','Mileage Km/L']].head(200).to_json(orient='columns')
        elif option == 2:
            jsonData = autoMPG[autoMPG['Transmission']=='Manual'][['Price','Mileage Km/L']].head(200).to_json(orient='columns')
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        return JsonResponse(jsonData,safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
# Top Expensive Brands
def queryTwo(request):
    if request.method == 'GET':
        # Use absolute path only
        sale = pd.read_csv(SALES_DATASET_ABSOLUTE_PATH)
        jsonData = sale.sort_values(by=['Avg Price'], ascending=False)[['Brand', 'Avg Price', 'Autogroup']].head(6).to_json(orient='records')
        return JsonResponse(jsonData,safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)

# URL Format `http://127.0.0.1:8000/cars/${make}/${fuelType}/${transmission}/${orderBy}/${year}/${mileageKML}/${engineCC}/${power}/${seats}/${price}/${noOfRecords/`

def FilteredCars(request, manufacturer, fuelType, transmission, orderBy, year, mileageKML, engineCC, power, seats, price, numberOfRecords):
    if request.method == 'GET':
        autoMPG = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
        # Adding AverageYearlySales Column to tell most popular car specification
        # Interquantile range calculated from sales data set to make random sales more relevant
            # iqr1 = df.quantile(0.25)
            # iqr2 = df.quantile(0.75)
            # iqr = iqr2 - iqr1
        #     => range = [iqr1,iqr]
        # adding sales column
        # iqr1 = 200000 approx and iqr = 800000
        # autoMPG['AverageYearlySales'] = np.random.randint(200000, 800000, autoMPG.shape[0])
        # using data set which already added random sales data for performance

        # # Removing Duplicates from CSV Data by NAME column
        # autoMPG = autoMPG.drop_duplicates(subset=['Name'], keep='first', inplace=False, ignore_index=False)
        # using data set which already added random sales data for performance


        # Manufacturer Filter
        if(manufacturer != 'All'):
            autoMPG = autoMPG[(autoMPG['Manufacturer'] == manufacturer)]
        # FuelType Filter
        if(fuelType != 'All'):
            autoMPG = autoMPG[(autoMPG['Fuel_Type'] == fuelType)]
        # Transmission Filter
        if (transmission != 'All'):
            autoMPG = autoMPG[(autoMPG['Transmission'] == transmission)]
        # OrderBy Filter
        if(orderBy == 'Mileage'):
            autoMPG = autoMPG.sort_values(by=['Mileage Km/L'], ascending=False)
        elif(orderBy == 'EngineCC'):
            autoMPG = autoMPG.sort_values(by=['Engine CC'], ascending=False)
        elif (orderBy != 'None'):
            autoMPG = autoMPG.sort_values(by=[orderBy],ascending=False)
        # Year >= filter
        if (year != 0):
            autoMPG = autoMPG[(autoMPG['Year'] >= year)]
        # MileageKML >= filter
        if(mileageKML != 0):
            autoMPG = autoMPG[(autoMPG['Mileage Km/L'] >= mileageKML)]
        # EngineCC >= filter
        if(engineCC != 0):
            autoMPG = autoMPG[(autoMPG['Engine CC'] >= engineCC)]
        # Power >= filter
        if(power != 0):
            autoMPG = autoMPG[(autoMPG['Power'] >= power)]
        # Seats >= filter
        if (seats != 0):
            autoMPG = autoMPG[(autoMPG['Seats'] >= seats)]
        # Price >= filter
        if(price != 0):
            autoMPG = autoMPG[(autoMPG['Price'] >= price)]

        # Price >= filter
        if(numberOfRecords != 0):
            autoMPG = autoMPG.head(numberOfRecords)

        jsonData = autoMPG.to_json(orient='records')
        return JsonResponse(jsonData,safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)



def queryThree(request):

    if request.method == 'GET':
        # Use absolute path only
        sale = pd.read_csv(SALES_DATASET_ABSOLUTE_PATH)
        sale['2019 sales'] = sale['Q1 2019'] + sale['Q2 2019'] + sale['Q3 2019']
        sale['2020 sales'] = sale['Q1 2020'] + sale['Q2 2020'] + sale['Q3 2020']
        drop_col = ['Avg Price', 'Q1 2019', 'Q2 2019', 'Q3 2019', 'Q4 2019', 'Q1 2020', 'Q2 2020', 'Q3 2020', 'Q4 2020',
                    'Autogroup']
        sale = sale.drop(drop_col, axis=1)
        sale['Total sales'] = sale['2019 sales'] + sale['2020 sales']
        sale = sale.sort_values(by='Total sales', axis=0, ascending=False)
        sale = sale.head(10)
        sale = sale.drop(['Total sales'], axis=1)
        jsonData = sale.to_json(orient='columns')
        return JsonResponse(jsonData,safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)
#
def queryFour(request):

    if request.method == 'GET':
        # Use absolute path only
        sale = pd.read_csv(SALES_DATASET_ABSOLUTE_PATH)
        sale['2019 sales'] = sale['Q1 2019'] + sale['Q2 2019'] + sale['Q3 2019']
        sale['2020 sales'] = sale['Q1 2020'] + sale['Q2 2020'] + sale['Q3 2020']
        drop_col = ['Avg Price', 'Q1 2019', 'Q2 2019', 'Q3 2019', 'Q4 2019', 'Q1 2020', 'Q2 2020', 'Q3 2020', 'Q4 2020',
                    'Autogroup']
        sale = sale.drop(drop_col, axis=1)
        sale['Total sales'] = sale['2019 sales'] + sale['2020 sales']
        sale["Percent Change"] = ((sale["2020 sales"] - sale["2019 sales"]) / sale["2019 sales"]) * 100
        decimals = 2
        sale['Percent Change'] = sale['Percent Change'].apply(lambda x: round(x, decimals))

        Top_5 = sale.nlargest(5,['Percent Change'])
        Bottom_5 = sale.nsmallest(5, ['Percent Change'])
        frames = [Top_5, Bottom_5]
        print(frames)
        top = pd.concat(frames)
        top = top.drop(['Total sales', '2020 sales', '2019 sales'], axis=1)
        jsonData = top.sort_values(by='Percent Change', ascending=True).to_json(orient='records')
        return JsonResponse(jsonData,safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)

#
def queryFive(request, option):

    if request.method == 'GET':
        df = pd.read_csv(TOP_COUNTRIES_DATA_ABSOLUTE_DATA)
        if(option<=2 and option>=0):
            # selecting top 5 requested columns
            df = df.iloc[:5, [0, option + 1]]
            df = df.sort_values(by=df.columns[1], ascending=False)
            jsonData = df.to_json(orient='columns')
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        return JsonResponse(jsonData,safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)

#
def querySix(request, option):

    if request.method == 'GET':
        if(option==0):
            df = pd.read_csv(CARS_DATA_ABSOLUTE_PATH)
            df = df.groupby(['Drivetrain'])['Model'].count()
            df = (100. * df / df.sum()).round(1)
            jsonData=df.to_json(orient="columns")
        elif(option==1):
            df =  pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
            df = df.groupby(['Transmission'])['Name'].count()
            df = (100. * df / df.sum()).round(1)
            jsonData = df.to_json(orient="columns")
        elif(option==2):
            df = pd.read_csv(CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH)
            df.rename(columns={'Unnamed: 0': 'Brand', 'Unnamed: 1': 'Segment',
                               }, inplace=True)
            df = df.drop(labels=[0], axis=0, index=None, columns=None, level=None, inplace=False, errors='raise')
            df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric)
            df['Sales'] = df.iloc[:, 0:].sum(axis=1)
            df = df.groupby(by='Segment')['Sales'].sum()
            df = (100. * df / df.sum()).round(1)
            jsonData = df.to_json(orient="columns")
        elif(option==3):
            df= pd.read_csv(SALES_DATASET_ABSOLUTE_PATH)
            df['Sales'] = df.iloc[:, 3:].sum(axis=1)
            df = df.groupby(by='Brand')['Sales'].sum()
            df = df.astype('int32')
            jsonData = df.head(8).to_json(orient="columns")
        elif(option==4):
            df = pd.read_csv(MPG_DATASET_ABSOLUTE_PATH)
            df = df.groupby(['Fuel_Type'])['Name'].count()
            df = (100. * df / df.sum()).round(1)
            jsonData = df.to_json(orient="columns")
        elif(option==5):
            df = pd.read_csv(CARS_DATA_ABSOLUTE_PATH)
            df = df.groupby(by="Body_Type")['Unnamed: 0'].count().sort_values(ascending=False)[0:9]
            df = (100. * df / df.sum()).round(1)


        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        return JsonResponse(jsonData,safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)

# Right Time to Launch Car Analysis
def querySeven(request,option):
    if request.method == 'GET':
        # Use absolute path only
        df = pd.read_csv(CARS_MONTHLY_SALES_DATA_ABSOLUTE_PATH)

        df.rename(columns={'Unnamed: 0': 'Brand', 'Unnamed: 1': 'Segment',
                           }, inplace=True)
        df = df.drop(labels=[0], axis=0, index=None, columns=None, level=None, inplace=False, errors='raise')
        df[df.columns[2:]] = df[df.columns[2:]].apply(pd.to_numeric)
        df['Jan'] = df['2019'] * .5 + df['2020'] * .5
        df['Feb'] = df['2019.1'] * .5 + df['2020.1'] * .5
        df['Mar'] = df['2019.2'] * .5 + df['2020.2'] * .5
        df['Apr'] = df['2019.3'] * .5 + df['2020.3'] * .5
        df['May'] = df['2019.4'] * .5 + df['2020.4'] * .5
        df['Jun'] = df['2019.5'] * .5 + df['2020.5'] * .5
        df['Jul'] = df['2019.6'] * .5 + df['2020.6'] * .5
        df['Aug'] = df['2019.7'] * .5 + df['2020.7'] * .5
        df['Sep'] = df['2019.8'] * .5 + df['2020.8'] * .5
        df['Oct'] = df['2019.8']
        df['Nov'] = df['2019.8']
        df['Dec'] = df['2019.8']
        convert_dict = {'Jan': int,
                        'Feb': int,
                        'Mar': int,
                        'Apr': int,
                        'May': int,
                        'Jun': int,
                        'Jul': int,
                        'Aug': int,
                        'Sep': int,
                        }

        df = df.astype(convert_dict)
        jan = df.groupby(by=['Segment'])['Jan'].sum()
        feb = df.groupby(by=['Segment'])['Feb'].sum()
        mar = df.groupby(by=['Segment'])['Mar'].sum()
        apr = df.groupby(by=['Segment'])['Apr'].sum()
        may = df.groupby(by=['Segment'])['May'].sum()
        jun = df.groupby(by=['Segment'])['Jun'].sum()
        jul = df.groupby(by=['Segment'])['Jul'].sum()
        aug = df.groupby(by=['Segment'])['Aug'].sum()
        sep = df.groupby(by=['Segment'])['Sep'].sum()
        oct = df.groupby(by=['Segment'])['Oct'].sum()
        nov = df.groupby(by=['Segment'])['Nov'].sum()
        dec = df.groupby(by=['Segment'])['Dec'].sum()
        frames = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
        result = pd.concat(frames, axis=1)
        result = result.T

        result['EconomySMA'] = result['Economy'].rolling(2).mean()
        result['LuxurySMA'] = result['Luxury'].rolling(2).mean()
        result['MidRangeSMA'] = result['Mid-Range'].rolling(2).mean()
        result['UltraLuxurySMA'] = result['Ultra Luxury'].rolling(2).mean()
        result['EconomyDiff'] = result['Economy']-result['EconomySMA']
        result['LuxuryDiff'] = result['Luxury']-result['LuxurySMA']
        result['MidRangeDiff'] = result['Mid-Range']-result['MidRangeSMA']
        result['UltraLuxuryDiff'] = result['Ultra Luxury']-result['UltraLuxurySMA']

        bestUltraLuxury = result.loc[result['UltraLuxurySMA'] < result['Ultra Luxury']].sort_values(
            by='UltraLuxuryDiff', ascending=False).head(3).iloc[0:3, 0:0]
        bestMidRange = result.loc[result['MidRangeSMA'] < result['Mid-Range']].sort_values(by='MidRangeDiff',
                                                                                           ascending=False).head(
            3).iloc[0:3, 0:0]
        bestEconomy = result.loc[result['EconomySMA'] < result['Economy']].sort_values(by='EconomyDiff',
                                                                                       ascending=False).head(3).iloc[
                      0:3, 0:0]
        bestLuxury = result.loc[result['LuxurySMA'] < result['Luxury']].sort_values(by='LuxuryDiff',
                                                                                    ascending=False).head(3).iloc[0:3,
                     0:0]
        framesBestMonths = [bestEconomy, bestLuxury, bestMidRange, bestUltraLuxury]
        print(framesBestMonths)
        bestMonths = pd.concat(framesBestMonths, axis=0)
        bestMonthsList = list(bestMonths.index.values)
        print(bestMonthsList)
        result = result.T
        result = result.round(0)
        if(option==1):
            jsonData = result.to_json(orient='records')
        else:
            jsonData = json.dumps(bestMonthsList)

        return JsonResponse(jsonData,safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)

def overview(request):
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

def queryEight(request):
    if request.method == 'GET':
        df = pd.read_csv(PRODUCTION_OF_VEHICLES_DATA_ABSOLUTE_PATH)
        df = df.loc[df['Indicators'] == 'Production of Passenger Cars (PV)'].sort_values('Year')
        pct_change_df = df['Value'].pct_change() * 100
        df = pd.concat([df, pct_change_df], axis=1)
        df.columns.values[3] = "Percent Change"
        df = df.round(1)
        df.drop("Indicators", axis=1, inplace=True)
        df.dropna(inplace=True)
        jsonData = df.to_json(orient="records")
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)

def queryNine(request):
    if request.method == 'GET':
        df = pd.read_csv(TOTAL_CAR_SALES_ABSOLUTE_PATH)
        jsonData = df.to_json(orient="columns");
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)

def queryTen(request, option):
    if request.method == 'GET':
        if(option==0):
            df = pd.read_csv(AUTOMAKERS_BY_EARNING_ABSOLUTE_PATH)
            df['earnings_ttm'] = df['earnings_ttm']/1000000000
            df = df.iloc[0:10, [1,3]]

        elif(option==1):
            df = pd.read_csv(AUTOMAKERS_BY_REVENUE_ABSOLUTE_PATH)
            df['revenue_ttm'] = df['revenue_ttm']/1000000000
            df = df.iloc[0:10, [1,3]]
        elif(option==2):
            df = pd.read_csv(AUTOMAKERS_BY_MARKET_CAPITALIZATION_ABSOLUTE_PATH)
            df['marketcap'] = df['marketcap'] / 1000000000
            df = df.iloc[0:10, [1, 3]]
        elif(option==3):
            df = pd.read_csv(AUTOMAKERS_BY_EMPLOYEES_ABSOLUTE_PATH)
            df = df.iloc[0:10, [1,3]]
        else:
            html = "<html><body>Incorrect URL</body></html>"
            return HttpResponse(html)
        df = df.round()
        jsonData = df.to_json(orient="columns");
        return JsonResponse(jsonData, safe=False)
    else:
        html = "<html><body>Only GET Method Allowed.</body></html>"
        return HttpResponse(html)

@api_view(['GET', 'POST'])
def forecastSales(request,p=1,q=1,steps=5, nlags=9):
    def test_stationarity(timeseries):
        dftest = adfuller(timeseries, autolag='AIC')
        dfoutput = pd.Series(dftest[0:4],
                             index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
        for key, value in dftest[4].items():
            dfoutput['Critical Value (%s)' % key] = value
        return dfoutput
    if request.method == 'POST':

        df = pd.read_csv(request.data['file_url'])
        # acf, pacf value
        # Selecting first two columns from uploaded dataset
        df = df.iloc[:, 0:2]
        # inferring datetime
        df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], infer_datetime_format=True, errors='coerce')
        # rename first col as datetime and second as sales
        df.columns = ['datetime', 'sales']
        # # indexing by datetime column
        indexedDataset = df.set_index(df['datetime'])
        # # perform dickey-fuller test for indexedDataset
        dfoutput = test_stationarity(indexedDataset['sales'])
        isStationary = dfoutput['Test Statistic'] < dfoutput['Critical Value (10%)'] and dfoutput['p-value']<=0.1
        # # indexedDataset_logScale
        temp = indexedDataset
        temp['sales'] = np.log(temp['sales'])
        indexedDataset_logScale = temp
        # perform df test for logScale indexeddataset
        test_stationarity(indexedDataset_logScale['sales'])
        dfoutputlog = test_stationarity(indexedDataset_logScale['sales'])
        isStationary = isStationary or (dfoutputlog['Test Statistic'] < dfoutputlog['Critical Value (10%)'] and dfoutputlog['p-value']<=0.1)
        # ACF and PACF
        # nlags depends on number of datapoints
        # Can only compute partial correlations for lags up to 50% of the sample size. The requested nlags 20 must be < 10.(in this case)
        # shifting
        datasetLogDiffShifting = indexedDataset_logScale - indexedDataset_logScale.shift()
        datasetLogDiffShifting.dropna(inplace=True)
        lag_acf = acf(datasetLogDiffShifting['sales'], nlags=nlags)
        lag_pacf = pacf(datasetLogDiffShifting['sales'], nlags=nlags, method='ols')

        model = ARIMA(indexedDataset_logScale['sales'], order=(p, 1, q))
        results_ARIMA = model.fit()
        # p value -> partial autocorrelation, d value -> autocorrlation
        # # RSA Value
        RSA_VALUE = sum(results_ARIMA.fittedvalues[1:]-datasetLogDiffShifting['sales'])**2
        RSA_VALUE = round(RSA_VALUE)
        # # predictions + data transformation
        predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
        # # convert to culmulative sum
        predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
        # # predictions + data transformation
        # # predictions in log scale
        predictions_ARIMA_log = pd.Series(indexedDataset_logScale['sales'], index=indexedDataset_logScale.index)
        predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum, fill_value=0)
        # # predictions in array format
        # # ignoring first record
        predictions = np.exp(results_ARIMA.predict())[1:]
        actual = np.exp(indexedDataset['sales'])[1:]
        # # error calculation
        # root mean squared error
        rmse = np.sqrt(mean_squared_error(actual, predictions))
        rmse = round(rmse)
        # converting mean absolute error to percentage
        mape = mean_absolute_percentage_error(actual, predictions)
        mape *= 100
        mape = round(mape)
        # #sales forecast
        forecast = np.exp(results_ARIMA.forecast(steps=steps))
        forecast = forecast.round()
        # converting bool to str
        isStationaryStr = str(isStationary)
        dataDict = {
            "RSA":RSA_VALUE,
            "RMSE": rmse,
            "MAPE": mape,
            "FORECAST": forecast.to_json(),
            "IS_STATIONARY": isStationaryStr,

        }
        jsonData = json.dumps(dataDict)
        return JsonResponse(jsonData, safe=False)
    else:
        return Response(request.data)
@api_view(['GET', 'POST'])
def post(request):
    if request.method == 'GET':
        html = "<html>GET</body></html>"
        return HttpResponse(html)
    elif request.method == 'POST':
        return Response(request.data['file_url'])

def apiHome(request):
    if request.method:
        html = "<html><body>API Working Fine</body></html>"
        return HttpResponse(html)

