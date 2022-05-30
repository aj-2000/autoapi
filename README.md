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

# API documentation

## 1. CARS
Responsible for funtioning of data analyzer.

**URL** : 
```url
/cars/{manufacturer}/{fuelType}/{transmission}/{orderBy}/{year}/{mileageKML}/{engineCC}/{power}/{seats}/{price}/{numberOfRecords}/
```

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

**Condition** : No records found.

**Code** : `200 OK`

**Content** : `{[]}`

### OR

**Condition** : records found.
#### Example
```
/cars/Maruti/Petrol/Automatic/Price/2018/0/0/0/0/5/1/
```
**Code** : `200 OK`

**Content** :

```json
[
    {
  "Unnamed: 0.1": 428,
  "Unnamed: 0": 431,
  "Name": "Maruti Baleno Alpha Automatic",
  "Manufacturer": "Maruti",
  "Location": "Coimbatore",
  "Year": 2018,
  "Kilometers_Driven": 12831,
  "Fuel_Type": "Petrol",
  "Transmission": "Automatic",
  "Owner_Type": "First",
  "Engine CC": 1197,
  "Power": 83.1,
  "Seats": 5,
  "Mileage Km/L": 21.4,
  "Price": 9.89,
  "AverageYearlySales": 498280
}
]
```