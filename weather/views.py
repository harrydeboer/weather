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
    curve = _get_curve(DataColumn.mean_temp, 1, first_year, last_year)
    data = _curve_to_json(curve)
    text_output = 'First day of summer: ' + curve.get_first_date_summer().strftime("%d %B") + '.'
    return render(request, 'temperature/index.html', {'data': data, 'text_output': text_output})


def temperature_year(request, first_year, last_year):
    curve = _get_curve(DataColumn.mean_temp, 0, first_year, last_year)
    data = _curve_to_json(curve)
    text_output = 'Temperature increase: ' + str(int((curve.y_smooth[-1] - curve.y_smooth[0]) * 10) / 10) + "°."
    return render(request, 'temperature/index.html', {'data': data, 'text_output': text_output})


def rain(request):
    return render(request, 'rain/index.html', {'data': [[]], 'text_output': ''})


def rain_amount(request, first_year, last_year):
    curve = _get_curve(DataColumn.amount_rain, 1, first_year, last_year)
    data = _curve_to_json(curve)
    return render(request, 'rain/index.html', {'data': data})


def rain_percentage(request, first_year, last_year):
    curve = _get_curve(DataColumn.perc_rain, 1, first_year, last_year)
    data = _curve_to_json(curve)
    return render(request, 'rain/index.html', {'data': data})


def wind(request):
    return render(request, 'wind/index.html', {'data': [[]], 'text_output': ''})


def wind_speed(request, first_year, last_year):
    curve = _get_curve(DataColumn.wind_speed, 1, first_year, last_year)
    data = _curve_to_json(curve)
    return render(request, 'wind/index.html', {'data': data})


def wind_vector(request, first_year, last_year):
    # The vector average speed and direction are retrieved as a 2 dimensional day year array.
    speed_2d = DayYearArrayBuildService.make_array(knmiData.array, first_year,
                                                   last_year, DataColumn.wind_speed_va)
    angle_2d = DayYearArrayBuildService.make_array(knmiData.array,
                                                   first_year, last_year, DataColumn.wind_direction)

    # The 2 dimensional angle and speed are averaged over the years.
    angle = Curve.mean_of_angle(speed_2d, angle_2d)

    curve = Curve(angle, True, first_year, last_year)
    data = _curve_to_json(curve)
    return render(request, 'wind/index.html', {'data': data})


def sunshine(request):
    return render(request, 'sunshine/index.html', {'data': [[]], 'text_output': ''})


def sunshine_percentage(request, first_year, last_year):
    curve = _get_curve(DataColumn.perc_sunshine, 1, first_year, last_year)
    data = _curve_to_json(curve)
    return render(request, 'sunshine/index.html', {'data': data})


def _get_curve(column_name, axis, first_year, last_year):
    array = DayYearArrayBuildService.make_array(knmiData.array, first_year, last_year, column_name)
    y = array.mean(axis=axis)
    return Curve(y, bool(axis), first_year, last_year)


def _curve_to_json(curve):
    data_array = np.array([curve.x, curve.y, curve.y_smooth])
    return json.dumps(np.transpose(data_array).tolist())
