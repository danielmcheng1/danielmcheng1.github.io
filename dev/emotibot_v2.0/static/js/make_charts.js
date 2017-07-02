

var emotionsToColor = {"anger": "red", "fear": "grey", "joy": "green", "sadness": "#000080", "surprise": "orange"}
var emotionsToData = {}
var emotions = Object.keys(emotionsToColor).sort()

var emotionsChartConfig = {
    type: 'line',
    data: {
        labels: [],
        datasets: []
        },
    options: {
        responsive: true,
        title:{
            display:true,
            text:'Conversation Emotions',
            fontSize: 18
        },
        legend: {
            display: true,
            position: 'top'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Response (#)',
                    fontSize: 14
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Probability (%)',
                    fontSize: 14
                },
                ticks: {
                    min: 0,
                    max: 100
                }
            }]
        }
    }
};


function refreshChartData_EmotionsWrapper(newData) {
    console.log(dataToPercent(newData));
    appendNewData(dataToPercent(newData), emotionsToData);
    refreshChartData(emotionsToData, emotionsToColor, emotionsChartConfig);
};

function refreshChartData(dataValues, dataColors, chartConfig) {
    //update vertical axes data values 
    var keys = Object.keys(dataValues).sort();
    chartConfig["data"]["datasets"] = []
    $.each(keys, function(index, item) {
        chartConfig["data"]["datasets"].push({
            label: item,
            backgroundColor: dataColors[item],
            borderColor: dataColors[item],
            data: dataValues[item],
            fill: false,
        });
    });
    
    //update horizontal axes labels based on length of the first dataset
    emotionsChartConfig["data"]["labels"] = []
    $.each(dataValues[keys[0]], function(index, item) {
        emotionsChartConfig["data"]["labels"].push(index + 1);
    });
    console.log(dataValues[keys[0]],    emotionsChartConfig["data"]["labels"])
    
    //refresh canvas 
    window.myLine.update();
};

function appendNewData(newData, currentData) {
    $.each(newData, function(index, item) {
        currentData[index].push(item);
    });
};

function numToPercent(num, digits) {
    return (num * 100).toFixed(digits)
};
function dataToPercent(data) {
    var rv = {}
    $.each(data, function(index, item) {
        rv[index] = numToPercent(item, 1);
    });
    return rv;
};

window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, emotionsChartConfig);
    $.each(emotions, function(index, item) {
        $('#checkboxes_emotion_chart').append(
           $(document.createElement('input')).attr({
               id:    'checkbox_' + item
              ,type:  'checkbox'
              ,checked: true
           })
        ).append('<label>' + item + '  </label>')
    });
    
        
    $.each(emotions, function(index, item) {
        emotionsToData[item] = [];
    });
    
    refreshChartData_EmotionsWrapper({});
};

document.getElementById('randomizeData').addEventListener('click', function() {
    config.data.datasets.forEach(function(dataset) {
        dataset.data = dataset.data.map(function() {
            return randomScalingFactor();
        });

    });
    window.myLine.update();
        
        
});
document.getElementById('addDataset').addEventListener('click', function() {
    var colorName = colorNames[config.data.datasets.length % colorNames.length];
    var newColor = chartColors[colorName];
    var newDataset = {
        label: 'Dataset ' + config.data.datasets.length,
        backgroundColor: newColor,
        borderColor: newColor,
        data: [],
        fill: false
    };

    for (var index = 0; index < config.data.labels.length; ++index) {
        newDataset.data.push(randomScalingFactor());
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
});

document.getElementById('addData').addEventListener('click', function() {
    if (config.data.datasets.length > 0) {
        var month = MONTHS[config.data.labels.length % MONTHS.length];
        config.data.labels.push(month);

        config.data.datasets.forEach(function(dataset) {
            dataset.data.push(randomScalingFactor());
        });

        window.myLine.update();
    }
});

document.getElementById('removeDataset').addEventListener('click', function() {
    config.data.datasets.splice(0, 1);
    window.myLine.update();
});

document.getElementById('removeData').addEventListener('click', function() {
    config.data.labels.splice(-1, 1); // remove the label first

    config.data.datasets.forEach(function(dataset, datasetIndex) {
        dataset.data.pop();
    });

    window.myLine.update();
});