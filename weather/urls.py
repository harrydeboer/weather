"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter
from weather.four_digit_year_converter import FourDigitYearConverter
import weather.views

register_converter(FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('', weather.views.index, name='home'),
    path('admin/', admin.site.urls),
    path('temperature', weather.views.temperature, name='temperature'),
    path('temperature-day/<yyyy:first_year>/<yyyy:last_year>/', weather.views.temperature_day, name='temperature_day'),
    path('temperature-year/<yyyy:first_year>/<yyyy:last_year>/',
         weather.views.temperature_year, name='temperature_year'),
    path('rain', weather.views.rain, name='rain'),
    path('rain-amount/<yyyy:first_year>/<yyyy:last_year>/', weather.views.rain_amount, name='rain_amount'),
    path('rain-percentage/<yyyy:first_year>/<yyyy:last_year>/', weather.views.rain_percentage, name='rain_percentage'),
    path('wind', weather.views.wind, name='wind'),
    path('wind-speed/<yyyy:first_year>/<yyyy:last_year>/', weather.views.wind_speed, name='wind_speed'),
    path('wind-vector/<yyyy:first_year>/<yyyy:last_year>/', weather.views.wind_vector, name='wind_vector'),
    path('sunshine', weather.views.sunshine, name='sunshine'),
    path('sunshine-percentage/<yyyy:first_year>/<yyyy:last_year>/',
         weather.views.sunshine_percentage, name='sunshine_percentage'),
]
