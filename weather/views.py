from django.shortcuts import render
from weather.models import Curve
from weather.services import DayYearArrayBuildService, DataColumn
from weather.models import KNMIData
import json
import numpy as np
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest

knmiData = KNMIData()

def index(request: WSGIRequest) -> HttpResponse:
    return render(request, 'homepage/index.html', {'data': [[]], 'text_output': ''})


def temperature(request: WSGIRequest) -> HttpResponse:
    return render(request, 'temperature/index.html', {'minYear': knmiData.minYearFile,
                                                      'maxYear': knmiData.maxYearFile, 'text_output': ''})


def temperature_day(request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
    data = {}
    curve = _get_curve(DataColumn.mean_temp, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['text_output'] = 'First day of summer: ' + curve.get_first_date_summer().strftime("%d %B") + '.'
    data['title'] = 'Temperature year curve'
    data['vertical'] = 'temperature °C'
    data['horizontal'] = 'year'
    return render(request, 'temperature/index.html', data)


def temperature_year(request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
    data = {}
    curve = _get_curve(DataColumn.mean_temp, 0, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['text_output'] = 'Temperature increase: ' + str(int((curve.y_smooth[-1] - curve.y_smooth[0]) * 10) / 10) + "°."
    data['title'] = 'Temperature year curve'
    data['vertical'] = 'temperature °C'
    data['horizontal'] = 'year'
    return render(request, 'temperature/index.html', data)


def rain(request: WSGIRequest) -> HttpResponse:
    return render(request, 'rain/index.html', {'minYear': knmiData.minYearFile,
                                                      'maxYear': knmiData.maxYearFile, 'text_output': ''})


def rain_amount(request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
    data = {}
    curve = _get_curve(DataColumn.amount_rain, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['title'] = 'Rain amount day curve'
    data['vertical'] = 'amount rain mm'
    data['horizontal'] = 'day number'
    return render(request, 'rain/index.html', data)


def rain_percentage(request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
    data = {}
    curve = _get_curve(DataColumn.perc_rain, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['title'] = 'Rain percentage day curve'
    data['vertical'] = 'percentage rain'
    data['horizontal'] = 'day number'
    return render(request, 'rain/index.html', data)


def wind(request: WSGIRequest) -> HttpResponse:
    return render(request, 'wind/index.html', {'minYear': knmiData.minYearFile,
                                                      'maxYear': knmiData.maxYearFile, 'text_output': ''})


def wind_speed(request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
    data = {}
    curve = _get_curve(DataColumn.wind_speed, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['title'] = 'Wind speed day curve'
    data['vertical'] = 'speed m/s'
    data['horizontal'] = 'day number'
    return render(request, 'wind/index.html', data)


def wind_vector(request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
    data = {}
    # The vector average speed and direction are retrieved as a 2-dimensional day year array.
    speed_2d = DayYearArrayBuildService.make_array(knmiData.array, first_year,
                                                   last_year, DataColumn.wind_speed_va)
    angle_2d = DayYearArrayBuildService.make_array(knmiData.array,
                                                   first_year, last_year, DataColumn.wind_direction)

    # The 2-dimensional angle and speed are averaged over the years.
    angle = Curve.mean_of_angle(speed_2d, angle_2d)

    curve = Curve(angle, True, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['title'] = 'Wind direction day curve'
    data['vertical'] = 'angle'
    data['horizontal'] = 'day number'
    return render(request, 'wind/index.html', data)


def sunshine(request: WSGIRequest) -> HttpResponse:
    return render(request, 'sunshine/index.html', {'minYear': knmiData.minYearFile,
                                                      'maxYear': knmiData.maxYearFile, 'text_output': ''})


def sunshine_percentage(request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
    data = {}
    curve = _get_curve(DataColumn.perc_sunshine, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['title'] = 'Sunshine day curve'
    data['vertical'] = 'percentage of sun'
    data['horizontal'] = 'day number'
    return render(request, 'sunshine/index.html', data)

def tropical(request: WSGIRequest) -> HttpResponse:
    return render(request, 'tropical/index.html', {'minYear': knmiData.minYearFile,
                                                      'maxYear': knmiData.maxYearFile, 'text_output': ''})

def tropical_year(request: WSGIRequest, first_year: int, last_year: int) -> HttpResponse:
    data = {}
    temperatures = DayYearArrayBuildService.make_array(knmiData.array, first_year, last_year, DataColumn.max_temp)
    data_temp = np.zeros(temperatures.shape[1])
    index_year = 0
    for year in np.transpose(temperatures):
        for temp in year:
            if temp >= 30:
                data_temp[index_year] += 1
        index_year += 1
    data['json'] = _curve_to_json(Curve(data_temp, False, first_year, last_year))
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['title'] = 'Tropical days curve'
    data['vertical'] = 'count'
    data['horizontal'] = 'year'
    return render(request, 'tropical/index.html', data)

def extreme(request: WSGIRequest) -> HttpResponse:
    data = {}
    rain_amounts = DayYearArrayBuildService.make_array(knmiData.array, 1930,
                                                       knmiData.maxYearFile, DataColumn.amount_rain)
    data_temp = np.zeros(rain_amounts.shape[1])
    index_year = 0
    rain_amount_average = 0
    for year in np.transpose(rain_amounts):
        for amount in year:
            rain_amount_average += amount
    rain_amount_average = rain_amount_average / len(np.transpose(rain_amounts))
    for year in np.transpose(rain_amounts):
        index_day = 0
        rain_amount_realized = 0
        deficit_days = np.zeros(len(year))
        for amount in year:
            rain_amount_average_day = rain_amount_average / 365.24 * (index_day + 1)
            rain_amount_realized += amount
            deficit_days[index_day] = rain_amount_realized - rain_amount_average_day
            index_day += 1
        data_temp[index_year] = np.max(deficit_days)
        index_year += 1
    data['json'] = _curve_to_json(Curve(data_temp, False, 1930, knmiData.maxYearFile))
    data['minYear'] = knmiData.minYearFile
    data['maxYear'] = knmiData.maxYearFile
    data['title'] = 'Max precipitation deficit'
    data['vertical'] = 'deficit'
    data['horizontal'] = 'year'
    return render(request, 'extreme/index.html', data)

def _get_curve(column_name: DataColumn, axis: int, first_year: int, last_year: int) -> Curve:
    array = DayYearArrayBuildService.make_array(knmiData.array, first_year, last_year, column_name)
    y = array.mean(axis=axis)
    return Curve(y, bool(axis), first_year, last_year)


def _curve_to_json(curve: Curve) -> str:
    data_array = np.array([curve.x, curve.y, curve.y_smooth])
    return json.dumps(np.transpose(data_array).tolist())
