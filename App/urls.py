from django.urls import path, include
from .views import queryOne, queryTwo, queryThree, queryFour, queryFive, querySix, querySeven, queryEight, queryNine, queryTen, FilteredCars, apiHome, overview, forecastSales, post
# queryThree, queryFour, queryFive, querySix, querySeven, apiHome
urlpatterns = [
    path('q1/<int:option>/', queryOne),
    path('q2/', queryTwo),
    # URL Format `http://127.0.0.1:8000/cars/${make}/${fuelType}/${transmission}/${orderBy}/${year}/${mileageKML}/${engineCC}/${power}/${seats}/${price}/${numberOfRecords}/`
    path('cars/<slug:manufacturer>/<slug:fuelType>/<slug:transmission>/<slug:orderBy>/<int:year>/<int:mileageKML>/<int:engineCC>/<int:power>/<int:seats>/<int:price>/<int:numberOfRecords>/', FilteredCars),
    path('q3/', queryThree),
    path('q4/', queryFour),
    path('q5/<int:option>', queryFive),
    path('q6/<int:option>', querySix),
    path('q7/<int:option>', querySeven),
    path('q8/', queryEight),
    path('q9/', queryNine),
    path('q10/<int:option>/', queryTen),
    path('forecast/<int:p>/<int:q>/<int:steps>/<int:nlags>/', forecastSales),
    path('overview/',overview),
    path('post/',post),
    path('', apiHome)
]
