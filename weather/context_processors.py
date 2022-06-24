from weather.models import KNMIData


def min_max_years(request):
    knmi_data = KNMIData()
    first_year = knmi_data.minYearFile
    last_year = knmi_data.maxYearFile
    return {'minYear': first_year, 'maxYear': last_year}
