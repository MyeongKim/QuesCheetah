import { highchart } from 'highcharts';
import { highstock } from 'highstock';

$('#side-nav-overview').addClass('active');

$.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function (data) {
    $('#container1').highcharts('StockChart', {
        rangeSelector: {
            selected: 1
        },
        title: {
            text: 'Answer count time chart'
        },

        series: [{
            name: 'AAPL',
            data: data,
            tooltip: {
                valueDecimals: 2
            }
        }]
    });
});

$('#container2').highcharts({
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Answers'
    },
    xAxis: {
        categories: ['Apples', 'Bananas', 'Oranges']
    },
    yAxis: {
        title: {
            text: 'Fruit eaten'
        }
    },
    series: [{
        name: 'Jane',
        data: [1, 0, 4]
    }, {
        name: 'John',
        data: [5, 7, 3]
    }]
});

$('.group-answer-bar-chart-btn button').click(function(){
    $('.group-answer-bar-chart-btn button').removeClass('active');
    $(this).addClass('active');
});
