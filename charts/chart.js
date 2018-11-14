function makePieChart(chartId, chartLabels, array) {
    var options = {
        chart: {
            width: 380,
            type: 'pie',
        },
        legend: {
            show: false,
        },
        series: array,
        labels: chartLabels,
    }
    eval(`var ${chartId} = new ApexCharts(document.querySelector("#${chartId}"), options );`);
    eval(`${chartId}.render();`);
}

function makeLineChart(chartId, chartLabels, array) {
    var options = {
        chart: {
            width: 380,
            type: 'line'
        },
        legend: {
            show: false,
        },
        series: array,
        labels: chartLabels, F
    }
    eval(`var ${chartId} = new ApexCharts(document.querySelector("#${chartId}"), options );`);
    eval(`${chartId}.render();`);
}

var switcher = true;

function pieChartToggler(chartId, tableId) {
    if (switcher) {
        transitionTime = 50;
        switcher = false;
        var row = document.getElementById(tableId + "Table");
        var cells = row.getElementsByTagName("th");
        var chartValues = [], chartTags = [];
        for (i = 0; i < cells.length; i++) {
            if (cells[i].className == "value") {
                chartValues.push(parseInt(cells[i].innerText));
            }
            else if (cells[i].className == "tag") {
                chartTags.push(cells[i].innerText);
            }
        }
        $("#" + tableId + "Table").hide(transitionTime);
        $("#" + tableId).css('background-image', 'linear-gradient(to left, rgba(255,255,255,0), rgba(0,0,0,0)');
        $("#" + chartId).show(100);
        // for 
        makePieChart(chartId, chartTags, chartValues);
    }
    else {
        switcher = true;
        $("#" + tableId + "Table").show(transitionTime);
        $("#" + tableId).css('background-image', 'none');
        $("#" + chartId).remove();
        $("#" + chartId + "Div").append('<div id="' + chartId + '" class="' + chartId + '"></div>');

    }
}

function lineChartToggler(chartId, tableId) {
    if (switcher) {
        transitionTime = 50;
        switcher = false;
        var row = document.getElementById(tableId + "Table");
        var cells = row.getElementsByTagName("th");
        var chartValues = [], chartTags = [];
        for (i = 0; i < cells.length; i++) {
            if (cells[i].className == "value") {
                chartValues.push(parseInt(cells[i].innerText));
            }
            else if (cells[i].className == "tag") {
                chartTags.push(cells[i].innerText);
            }
        }
        $("#" + tableId + "Table").hide(transitionTime);
        $("#" + tableId).css('background-image', 'linear-gradient(to left, rgba(255,255,255,0), rgba(0,0,0,0)');
        $("#" + chartId).show(100);
        // for 
        makeLineChart(chartId, chartTags, chartValues);
    }
    else {
        switcher = true;
        $("#" + tableId + "Table").show(transitionTime);
        $("#" + tableId).css('background-image', 'none');
        $("#" + chartId).remove();
        $("#" + chartId + "Div").append('<div id="' + chartId + '" class="' + chartId + '"></div>');

    }
}
// function chart2TableToggle()