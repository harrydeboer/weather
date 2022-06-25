from django.shortcuts import render
from weather.models import Curve
from weather.services import DayYearArrayBuildService, DataColumn
from weather.models import KNMIData
import json
import numpy as np

knmiData = KNMIData()


def index(request):
    return render(request, 'homepage/index.html', {'data': [[]], 'text_output': ''})


def temperature(request):
    return render(request, 'temperature/index.html', {'data': [[]], 'text_output': ''})


def temperature_day(request, first_year, last_year):
    data = {}
    curve = _get_curve(DataColumn.mean_temp, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['text_output'] = 'First day of summer: ' + curve.get_first_date_summer().strftime("%d %B") + '.'
    data['title'] = 'Temperature year curve'
    data['vertical'] = 'temperature °C'
    data['horizontal'] = 'year'
    return render(request, 'temperature/index.html', data)


def temperature_year(request, first_year, last_year):
    data = {}
    curve = _get_curve(DataColumn.mean_temp, 0, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['text_output'] = 'Temperature increase: ' + str(int((curve.y_smooth[-1] - curve.y_smooth[0]) * 10) / 10) + "°."
    data['title'] = 'Temperature year curve'
    data['vertical'] = 'temperature °C'
    data['horizontal'] = 'year'
    return render(request, 'temperature/index.html', data)


def rain(request):
    return render(request, 'rain/index.html', {'data': [[]], 'text_output': ''})


def rain_amount(request, first_year, last_year):
    data = {}
    curve = _get_curve(DataColumn.amount_rain, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['title'] = 'Rain amount day curve'
    data['vertical'] = 'amount rain mm'
    data['horizontal'] = 'day number'
    return render(request, 'rain/index.html', data)


def rain_percentage(request, first_year, last_year):
    data = {}
    curve = _get_curve(DataColumn.perc_rain, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['title'] = 'Rain percentage day curve'
    data['vertical'] = 'percentage rain'
    data['horizontal'] = 'day number'
    return render(request, 'rain/index.html', data)


def wind(request):
    return render(request, 'wind/index.html', {'data': [[]], 'text_output': ''})


def wind_speed(request, first_year, last_year):
    data = {}
    curve = _get_curve(DataColumn.wind_speed, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['title'] = 'Wind speed day curve'
    data['vertical'] = 'speed m/s'
    data['horizontal'] = 'day number'
    return render(request, 'wind/index.html', data)


def wind_vector(request, first_year, last_year):
    data = {}
    # The vector average speed and direction are retrieved as a 2 dimensional day year array.
    speed_2d = DayYearArrayBuildService.make_array(knmiData.array, first_year,
                                                   last_year, DataColumn.wind_speed_va)
    angle_2d = DayYearArrayBuildService.make_array(knmiData.array,
                                                   first_year, last_year, DataColumn.wind_direction)

    # The 2 dimensional angle and speed are averaged over the years.
    angle = Curve.mean_of_angle(speed_2d, angle_2d)

    curve = Curve(angle, True, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['title'] = 'Wind direction day curve'
    data['vertical'] = 'angle'
    data['horizontal'] = 'day number'
    return render(request, 'wind/index.html', data)


def sunshine(request):
    return render(request, 'sunshine/index.html', {'data': [[]], 'text_output': ''})


def sunshine_percentage(request, first_year, last_year):
    data = {}
    curve = _get_curve(DataColumn.perc_sunshine, 1, first_year, last_year)
    data['json'] = _curve_to_json(curve)
    data['title'] = 'Sunshine day curve'
    data['vertical'] = 'percentage of sun'
    data['horizontal'] = 'day number'
    return render(request, 'sunshine/index.html', data)


def _get_curve(column_name, axis, first_year, last_year):
    array = DayYearArrayBuildService.make_array(knmiData.array, first_year, last_year, column_name)
    y = array.mean(axis=axis)
    return Curve(y, bool(axis), first_year, last_year)


def _curve_to_json(curve):
    data_array = np.array([curve.x, curve.y, curve.y_smooth])
    return json.dumps(np.transpose(data_array).tolist())
