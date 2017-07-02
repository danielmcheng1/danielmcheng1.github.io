

var emotionsDataConfig = {
    colors: {"anger": "red", "fear": "grey", "joy": "green", "sadness": "#000080", "surprise": "orange"},
    dataValues: {},
    plotFlags: {}
};
var emotions = Object.keys(emotionsDataConfig["colors"]).sort();

var emotionsChartObject;
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
    appendNewData(dataToPercent(newData), emotionsDataConfig["dataValues"]);
    refreshChartData(emotionsDataConfig, emotionsChartConfig, emotionsChartObject);
};

function refreshChartData(dataConfig, chartConfig, chartObject) {
    //update vertical axes data values 
    var keys = Object.keys(dataConfig["dataValues"]).sort().filter(function(elem) {
        return dataConfig["plotFlags"][elem] === true; //don't plot any datasets that have been previously unchecked by user
    });
    
    chartConfig["data"]["datasets"] = []
    $.each(keys, function(index, item) {
        var color = dataConfig["colors"][item]
        var dataValue = dataConfig["dataValues"][item]
        chartConfig["data"]["datasets"].push({
            label: item,
            backgroundColor: color,
            borderColor: color,
            data: dataValue,
            fill: false,
        });
    });
    
    //update horizontal axes labels based on length of the first dataset
    chartConfig["data"]["labels"] = []
    $.each(dataConfig["dataValues"][keys[0]], function(index, item) {
        chartConfig["data"]["labels"].push(index + 1);
    });
    
    //refresh canvas 
    window.emotionsChartObject.update();
};

function appendNewData(newData, cumulativeData) {   
    $.each(newData, function(index, item) {
        //dataConfig["dataValues"][index].push(item);
        //do not use push because chart js automatically adds event listeners to trigger updates incorrectly (addEventListener in Chart.bundle.js)
        var currLen = cumulativeData[index].length;
        cumulativeData[index][currLen] = item;
    });
};

function numToPercent(num, digits) {
    return (num * 100).toFixed(digits)
};
function dataToPercent(data) {
    var toPercent = {}
    $.each(data, function(index, item) {
        toPercent[index] = numToPercent(item, 1);
    });
    return toPercent;
};



function addDataset(label, dataConfig, chartConfig, chartObject) {
    //mark this so that all future chart updates will plot this data 
    dataConfig["plotFlags"][label] = true;
    refreshChartData(dataConfig, chartConfig, chartObject)
};

function removeDataset(label, dataConfig, chartConfig, chartObject) {
    //mark this so that all future chart updates won't plot this data 
    dataConfig["plotFlags"][label] = false;
    refreshChartData(dataConfig, chartConfig, chartObject);  
};

window.onload = function() {
    //initialize the data objects for plotting emotions 
    $.each(emotions, function(index, item) {
        emotionsDataConfig["dataValues"][item] = [];
        emotionsDataConfig["plotFlags"][item] = true;
    });
    
    //set up charting canvas 
    var ctx = document.getElementById("canvas").getContext("2d");
    emotionsChartObject = new Chart(ctx, emotionsChartConfig);
    
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
            if (this.checked) addDataset(item, emotionsDataConfig, emotionsChartConfig, emotionsChartObject);
            else removeDataset(item, emotionsDataConfig, emotionsChartConfig, emotionsChartObject);           
        });
    });    
    
    //load initial blank data
    refreshChartData_EmotionsWrapper({});
};