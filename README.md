# autoapi
A REST api written in Django for Microsoft Engage 2022 Data Analysis Project.
> [AUTOAPI Service & Docs](https://engage-autoapi.herokuapp.com)

## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs
* [pandas](https://pandas.pydata.org/): pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.
* [NumPy](https://numpy.org/): NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.
* [Stats Model](https://www.statsmodels.org/stable/index.html): statsmodels is a Python module that provides classes and functions for the estimation of many different statistical models, as well as for conducting statistical tests, and statistical data exploration. An extensive list of result statistics are available for each estimator.

## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```bash
        pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```bash
        git clone https://github.com/aj-2000/autoapi.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            cd autoapi
        ```
    2. Create and fire up your virtual environment:
    
        LINUX/UNIX:
        ```bash
            virtualenv  venv -p python3
            source venv/bin/activate
        ```
        WINDOWS:
        ```bash
            virtualenv  venv -p python3
            venv\Scripts\activate
        
    3. Install the dependencies needed to run the app:
        ```bash
            pip install -r requirements.txt
        ```

* #### Run It
    Fire up the server using this one simple command:
    
    Development Server:
    ```bash
        python manage.py runserver
    ```
    Production Server:
    ```bash
        gunicorn autoapi.wsgi
    ```

    You can now access the autoapi service on your browser by using
    ```
        http://localhost:8000/
    ```
* #### Save your own Django SECRET KEY to .env file
    ```
    Inside /autoapi/.env
    SECRET KEY = "YOUR SECRET KEY"
    ```

# API documentation

## 1. CARS
Responsible for funtioning of data analyzer.

**URL** : 
```url
GET /cars/{manufacturer}/{fuelType}/{transmission}/{orderBy}/{year}/{mileageKML}/{engineCC}/{power}/{seats}/{price}/{numberOfRecords}/
```

**Method** : `GET`

**Auth required** : NO


## 2. OVERVIEW
Responsible for Dashboard Overview section.

**URL** : 
```url
/overview
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : `{}`

## Success Response

**Code** : `200 OK`

**Content** :

```json
    {
      "sales": "{\"2016\":159828.41,\"2017\":166812.66,\"2018\":166025.13,\"2019\":171464.76,\"2020\":161056.21,\"2021\":167303.02,\"January_2022\":34149.76,\"February_2022\":32607.59,\"March_2022\":31169.34,\"April_2022\":33017.0,\"May_2022\":33382.22,\"June_2022\":33658.23,\"2022\":197984.14}",
      "top_brand_of_year": "Maruti Suzuki",
      "top_brand_of_month": "Fiat"
    }
```

# 3. FORECAST
Responsible for Sales forecast  feature.

**URL** : `POST /forecast/{p}/{q}/{steps}/{option}
`


| Parameter | Description                                                                   |
|:---------:|:-----------------------------------------------------------------------------:|
| p         | P Value                                                                       |
| q         | Q Value                                                                       |
| steps     | Number of forecasts                                                           |
| option    | (1:Model Accuracy Chart Data), (2 : Model-Error Details), (3 : Forecast Data) |


**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data constraints**

Provide CSV dateset static file URL.

```json
{
    "file_url": "CSV FILE STATIC URL"
}
```

**Data example** All fields must be sent.

```json
{
    "file_url": "https://raw.githubusercontent.com/aj-2000/autoapi/main/App/datasets/demo_sales_dataset.csv"
}
```


## 4. Price and Mileage Data 
Responsible for Price vs Relation analysis Chart.

**URL** : 
```
GET /q1/{option}
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

| Parameter | Description                 |
|:---------:|:---------------------------:|
| option    | (1: Automatic), (2: Manual) |

## 5. Top 5 Expensive Brands Data
Responsible for Top 5 expensive brands table.
**URL** : 
```
GET /q2
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None


## 6. 2019 And 2020 Sales Data Of Top 10 Brands
Responsible for Price vs Relation analysis.

**URL** : 
```
GET /q3
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None


## 7. Sales Percentage Data
Responsible for Brand Performance Analysis

**URL** : 
```
GET /q4
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None


## 8. Top Countries Data
Responible for Top Countries Data Pie Chart.

**URL** : 
```
GET /q5/{option}
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

| Parameter |                    Description                     |
|:---------:|:--------------------------------------------------:|
| option    | (0: by production), (1: by sales), (2: by exports) |


## 9. Customer Segments Data
Responsible for Customer Segments Pie Chart.

**URL** : 
```
GET /q6/{option}
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

| Parameter |                                             Description                                      |
|:---------:|:--------------------------------------------------------------------------------------------:|
| option    | (0: Drive Train), (1: Transmission), (2: Class), (3: Brands), (4: Fuel Type), (5: By BodyTpe)|
## 10. Right Time To Launch Analysis Data
Responsible for Right Time to Launch Analysis Data

**URL** : 
```url
GET /q7/{option}
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None


| Parameter |               Description                |
|:---------:|:----------------------------------------:|
| option    | (1: Analysis Data), (2: Prediction Data) |

## 11. Passengers Car's Production Data 
Responsible for Growth of passengers cars produced in India.

**URL** : 
```url
GET /q8
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None


## 12. Consumer Sentiment And Sales Data
Responsible for Consumer Sentiment vs Sales Analysis Chart.

**URL** : 
```url
GET /q9
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None


## 13. Top Automakers Data
Responsible for Top Automakers Pie chart Data

**URL** : 
```url
GET /q10/{option}
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None


| Parameter |                                   Description                                   |
|:---------:|:-------------------------------------------------------------------------------:|
| option    | (0: by earnings), (1: by revenue), (2: by market cap.), (2: by employees count) |

