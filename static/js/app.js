url = window.location.href.split('/')

if (url[4] !== undefined ) {
    $('#firstYear').val(url[4])
    $('#lastYear').val(url[5])
}

$('.button').on('click', function (event) {

    let minYear = $('#minYear').val();
    let maxYear = $('#maxYear').val();
    let firstYear = $('#firstYear').val();
    let lastYear = $('#lastYear').val();
    let errorMessage = $('#error-message')

    if (lastYear < firstYear) {
        errorMessage.html('Last year cannot be smaller than first year.');
    } else if (firstYear < minYear || lastYear > maxYear) {
        errorMessage.html('Years out of range ' + minYear + '-' + maxYear + '.');
    } else if ($(this).data('url') === 'rain-percentage' && firstYear < 1930) {
        errorMessage.html('Range cannot be before 1930.');
    } else if ($(this).data('url') === 'temperature-year' && lastYear - firstYear + 1 < 9 ) {
        errorMessage.html('Range should be 9 years at least when making a year curve.');
    } else {
        window.location.href = '/' + $(this).data('url') + '/' + firstYear + '/' + lastYear;
    }

    event.preventDefault();
});

function graph(title, vertical, horizontal) {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(function(){ drawChart(title, vertical, horizontal) });
}

function drawChart(title, vertical, horizontal) {
    let data = google.visualization.arrayToDataTable(
        [['x', 'y', 'ysmooth']].concat($('#curveData').data('chart'))
    );

    let options = {
        title: title,
        curveType: 'function',
        vAxis: { title: vertical },
        hAxis: { title: horizontal},
        legend: { position: 'bottom' }
    };

    let chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}

if ($('#curve_chart').length > 0) {
    graph($('#graph-title').val(), $('#graph-vertical').val(), $('#graph-horizontal').val())
}
