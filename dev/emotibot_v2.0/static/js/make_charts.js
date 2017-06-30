

var emotionsToColor = {"anger": "red", "fear": "gray", "joy": "orange", "sadness": "blue", "surprise": "purple"}
var emotionsToData = {"anger": [0.1, 0.2, 0.3, 0.1234, 0.5], "fear": [1, 0.9, 0.1, 0.2, 0.2234]}
var emotions = Object.keys(emotionsToColor).sort()
function randomScalingFactor() {
    return Math.random()
}
//var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var MONTHS = [0, 1, 3, 10]
var config = {
    type: 'line',
    data: {
        labels: [0, 1, 2, 3, 4],
        datasets: [{
            label: emotions[0],
            backgroundColor: emotionsToColor[emotions[0]],
            borderColor: emotionsToColor[emotions[0]],
            data: emotionsToData[emotions[0]],
            fill: false,
        }, {
            label: emotions[1],
            fill: false,
            backgroundColor: emotionsToColor[emotions[1]],
            borderColor: emotionsToColor[emotions[1]],
            data: emotionsToData[emotions[1]],
        }]
    },
    options: {
        responsive: true,
        title:{
            display:true,
            text:'Emotions Throughout Conversation'
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
                    labelString: 'Response #'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Probability'
                }
            }]
        }
    }
};

window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
};

document.getElementById('randomizeData').addEventListener('click', function() {
    config.data.datasets.forEach(function(dataset) {
        dataset.data = dataset.data.map(function() {
            return randomScalingFactor();
        });

    });

    window.myLine.update();
});

var colorNames = Object.keys(chartColors);
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