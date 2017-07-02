

var emotionsToColor = {"anger": "red", "fear": "grey", "joy": "green", "sadness": "#000080", "surprise": "orange"}
var emotionsToData = {}
var emotionsToPlot = {}
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
    appendNewData(dataToPercent(newData), emotionsToData);
    refreshChartData(emotionsToData, emotionsToColor, emotionsChartConfig);
};

function refreshChartData(dataValues, dataColors, chartConfig) {
    //update vertical axes data values 
    var keys = Object.keys(dataValues).sort().filter(function(elem) {
        return dataToPlot[elem] === true; //don't plot any datasets that have been previously unchecked by user
    });
    
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
    //initialize the data objects for plotting emotions 
    $.each(emotions, function(index, item) {
        emotionsToData[item] = [];
        emotionsToPlot[item] = true;
    });
    
    //set up charting canvas 
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, emotionsChartConfig);
    
    //create checkboxes for selecting/deselecting each emotion 
    $.each(emotions, function(index, item) {
        $('#checkboxes_emotion_chart').append(
           $(document.createElement('input')).attr({
               id:    'checkbox_' + item
              ,type:  'checkbox'
              ,checked: true
           })
        ).append('<label>' + item + '  </label>')
        
        $('#checkbox_' + item).change(function() {
            console.log(item, this.checked);
            if (this.checked) addDataset(item, emotionsToPlot, emotionsChartConfig);
            else removeDataset(item, emotionsToPlot, emotionsChartConfig);            
        });
    });    
    
    //load initial blank data
    refreshChartData_EmotionsWrapper({});
};
function addDataset(label) {
    dataToPlot[label] = true;
    refreshChartData(emotionsToData, emotionsToColor, emotionsChartConfig);
};

function removeDataset(label) {
    //mark this so that all future chart updates won't plot this data 
    dataToPlot[label] = false;
    
    refreshChartData(emotionsToData, emotionsToColor, emotionsChartConfig);
    
    /*
    //now remove this from the currently displayed chart
    var indexToRemove = -1;
    $.each(chartConfig["data"]["datasets"], function(index, item) {
        if (item["label"] == label) {
            indexToRemove = index;
        };
    });
    if (indexToRemove != -1) {
        chartConfig["data"]["datasets"].splice(index, 1);
    }; 
    */   
};