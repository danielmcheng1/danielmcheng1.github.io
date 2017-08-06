function getStats() {
    return document.getElementById("statsChartDiv");
};
function statsExists() {
    return getStats() !== null;
};
function removeStats() {
    if (statsExists()) {
        getStats().remove();
        removeHiddenChartFrames();
    };
};

function removeHiddenChartFrames() {
    var hiddenFrames = document.getElementsByClassName("chartjs-hidden-iframe");
    for (var i = 0; i < hiddenFrames.length; i++) {
        hiddenFrames[i].remove();
    };
};
/*
Sizing issues with chart js. Try the following:
    place canvas in div
    options: {
    responsive: false}
    Chart.defaults.global.maintainAspectRatio = false;
*/
function appendStats(data) {
    //create wrapper so that we can control sizing 
    var canvasDiv = document.createElement("div");
    canvasDiv.setAttribute("id", "statsChartDiv");
    document.body.appendChild(canvasDiv);
    if (data != {}) {
        var canvasElement = document.createElement("canvas");
        canvasElement.setAttribute("id", "statsChart");
        canvasDiv.appendChild(canvasElement);
        
        var statsConfig = refreshStatsChartConfig(data);
        
        var canvasContext = document.getElementById("statsChart").getContext("2d");
        chartObject = new Chart(canvasContext, statsConfig);
        chartObject.update();
    };
};

function refreshStatsChartConfig(data) {
    var keysOrdered = Object.keys(data).sort(function(a, b) {
        return a - b;
    });
    var fullLevelNames = [];
    var livesUsed = [];
    for (var i = 0; i < keysOrdered.length; i++) {
        var charKey = keysOrdered[i];
        fullLevelNames.push(["Level " + charKey + ":", data[charKey]["levelName"]]);
        livesUsed.push(data[charKey]["livesUsed"]);
    };
    
    var dataConfig = {
        labels: fullLevelNames,
        datasets: [{
            label: 'Lives Used',
            backgroundColor: '#add8e6',
            borderColor: '#add8e6',
            borderWidth: 0,
            data: livesUsed
        }],

    };
    var config = {
        type: 'bar',
        data: dataConfig,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 5
                    }
                }]
            }
        }
    }
    return config;
};

