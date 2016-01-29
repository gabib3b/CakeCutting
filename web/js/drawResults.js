

function drawgraph22(data, xlabel, yLabel) {
  
    xValues = []
    yValues = []

    for (i = 0; i < data.values.length; i++) {
        xValues.push(data.values[i].X);
        yValues.push(data.values[i].Y);
    }

    var layout = {
        xaxis: {
            title: xlabel
        },
        yaxis: {
            title: yLabel,
            type: 'log'
        },
        margin: {
            t: 20
        },
        hovermode: 'closest'
    };

    var data = [{
        x: xValues,
        y: yValues,
        type: 'scatter'
    }
    ];


    Plotly.newPlot('myDiv', data, layout);
}


function drawgraph(data, xlabel, yLabel) {
    
    var graphDivId = createGrapgDiv();
    xValues = []
    yValues = []

    for (i = 0; i < data.values.length; i++) {
        xValues.push(data.values[i].X);
        yValues.push(data.values[i].Y);
    }

    var layout = {
        xaxis: {
            title: xlabel
        },
        yaxis: {
            title: yLabel,
            type: 'log'
        },
        margin: {
            t: 20
        },
        hovermode: 'closest'
    };

    var data = [{
        x: xValues,
        y: yValues,
        type: 'scatter'
    }
    ];


    Plotly.newPlot(graphDivId, data, layout);
}

var index = 1;
function createGrapgDiv() {
    var containerDiv = document.getElementById("results_container");
    var resultDiv = document.createElement('div');
    var id = 'graph_' + index;
    resultDiv.id = id;
    $(resultDiv).addClass("result-container");
    containerDiv.appendChild(resultDiv);
    index++;
    return id;
}

function clear() {
    $("#results_container").html("");
    index = 1;
}
