$(function () {
    // var bar_data defined in results.html
    // var plot_data defined in results.html
    var labels = ["Mid-season, successful", "Mid-season, re-injured", "Off-season, successful", "Off-season, re-injured"];
    var colors = [ "#2c9f42", "#ffc800", "#2575ed", "#ef969d" ];
    var seriesERA = [];
    var seriesFast = [];

    for (l in plot_data) {
        seriesERA.push({
            name: labels[l],
            color: colors[l],
            data: plot_data[l][0]
        });  
        seriesFast.push({
            name: labels[l],
            color: colors[l],
            data: plot_data[l][1]
        });         
    }

    $("#graph_era").highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: 'Days Off vs Change in ERA'
        },
        legend: {
            align: 'right',
            verticalAlign: 'top',
            layout: 'vertical',
            x: 0,
            y: 100,
            floating: true,
            itemStyle: {
                "fontWeight": "normal",
                "fontSize": "8px"
            }
        },
        tooltip: {
            pointFormat: "Days: {point.x}, ERA Diff: {point.y:.2f}"
        },
        xAxis: {
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true,
            title: { text: '# of Days' }
        },
        yAxis: {
            title: { text: 'Difference in ERA' }
        },
        series: seriesERA
    });

    $("#graph_fastball").highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: 'Days Off vs Change in Fastball Velocity'
        },
        legend: {
            align: 'right',
            verticalAlign: 'top',
            layout: 'vertical',
            x: 0,
            y: 100,
            floating: true,
            itemStyle: {
                "fontWeight": "normal",
                "fontSize": "8px"
            }
        },
        tooltip: {
            pointFormat: "Days: {point.x}, Fastball Diff: {point.y:.2f}"
        },
        xAxis: {
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true,
            title: { text: '# of Days' }
        },
        yAxis: {
            title: { text: 'Difference in ERA' }
        },
        series: seriesFast
    });

    $("#graph-labels").highcharts({
        chart: { type: 'bar' },
        title: {
            text: 'Number of Recovery Cases Per Category',
            style: 'fontSize: 14px'
        },
        legend: { enabled: false },
        xAxis: { categories: labels , title: { text: null }},
        yAxis: {
            min: 0,
            title: {
                text: '# Of Cases'
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        series: [{
            name: 'Number of Days',
            data: bar_data
        }]
    })

    function toggle_series(selector, sidxs){
        var chart = $(selector).highcharts();
        var hidden = false;
        
        for (idx in sidxs) {
            series = chart.series[sidxs[idx]];
            if (series.visible) {
                series.hide();
                hidden = true;
            } else {
                series.show();
            }
        }
        return hidden;
    }


    $('#figure-btn').click(function () {    
        var hidden = toggle_series('#graph_fastball', [2,3]);
        toggle_series('#graph_era', [2,3]);
        console.log(hidden);
        if (hidden){
            $(this).text("Show all data");
        } else {
            $(this).text("Show only mid-season points");
        };
    });

})




