
var xPadding = 30;
var yPadding = 30;
/*var data = {
    values: [{
        X: 0.2,
        Y: 1.4408
    }, {
        X: 0.4,
        Y: 1.110223
    }, {
        X: 0.6,
        Y: 2.2222
    }, {
        X: 0.8,
        Y: 2.61102
    }]
};*/




// Returns the max Y value in our data list
function getMaxY(data) {
    var max = 0;

    for (var i = 0; i < data.values.length; i++) {
        if (data.values[i].Y > max) {
            max = data.values[i].Y;
        }
    }

    max += 10 - max % 10;
    return max;
}

// Returns the max X value in our data list
function getMaxX(data) {
    var max = 0;

    for (var i = 0; i < data.values.length; i++) {
        if (data.values[i].X > max) {
            max = data.values[i].X;
        }
    }

    // omited
    //max += 10 - max % 10;
    return max;
}

// Return the x pixel for a graph point
function getXPixel(val, data) {
    // uses the getMaxX() function
    return ((graph.width - xPadding) / (getMaxX(data) + 1)) * val + (xPadding * 1.5);
    // was
    //return ((graph.width - xPadding) / getMaxX()) * val + (xPadding * 1.5);
}

// Return the y pixel for a graph point
function getYPixel(val, data) {
    return graph.height - (((graph.height - yPadding) / getMaxY(data)) * val) - yPadding;
}




function drawResults(graph, tipCanvas, data, xlabel, yLabel) {
    //var graph = document.getElementById("graph");
    var ctx = graph.getContext("2d");
    //var tipCanvas = document.getElementById("tip");
    var tipCtx = tipCanvas.getContext("2d");

    var canvasOffset = $(graph).offset();
    var offsetX = canvasOffset.left;
    var offsetY = canvasOffset.top;

    //var graph;



    // define tooltips for each data point
    var dots = [];
    for (var i = 0; i < data.values.length; i++) {
        dots.push({
            x: getXPixel(data.values[i].X, data),
            y: getYPixel(data.values[i].Y, data),
            orgX: data.values[i].X,
            orgY: data.values[i].Y,
            r: 4,
            rXr: 16,
            color: "red",
            tip: "#text" + (i + 1)
        });
    }

    // request mousemove events mousedown
    $(graph).mousemove(function (e) {
        handleMouseMove(e);
    });

    // show tooltip when mouse hovers over dot
    function handleMouseMove(e) {
        mouseX = parseInt(e.clientX - offsetX);
        mouseY = parseInt(e.clientY - offsetY);

        // Put your mousemove stuff here
        var hit = false;
        for (var i = 0; i < dots.length; i++) {
            var dot = dots[i];
            var dx = mouseX - dot.x;
            var dy = mouseY - dot.y;
            if (dx * dx + dy * dy < dot.rXr) {
                tipCanvas.style.left = (dot.x) + "px";
                tipCanvas.style.top = (dot.y - 40) + "px";
                tipCtx.clearRect(0, 0, tipCanvas.width, tipCanvas.height);
                //tipCtx.rect(0,0,tipCanvas.width,tipCanvas.height);
                //tipCtx.fillText($(dot.tip).val(), 5, 15);

                tipCtx.fillText(xlabel + ' -> ' + dot.orgX + '   ' + yLabel + ' -> ' + dot.orgY, 5, 15);

                hit = true;
            }
        }
        if (!hit) {
            tipCanvas.style.left = "-200px";
            tipCtx.clearRect(0, 0, tipCanvas.width, tipCanvas.height);
        }
    }


    // unchanged code follows

    //graph = document.getElementById("graph");
    var c = graph.getContext('2d');

    c.lineWidth = 2;
    c.strokeStyle = '#333';
    c.font = 'italic 8pt sans-serif';
    c.textAlign = "center";

    // Draw the axises
    c.beginPath();
    c.moveTo(xPadding, 0);
    c.lineTo(xPadding, graph.height - yPadding);
    c.lineTo(graph.width, graph.height - yPadding);
    c.stroke();

    // Draw the X value texts
    var myMaxX = getMaxX(data);
    for (var i = 0; i <= myMaxX; i++) {
        // uses data.values[i].X
        c.fillText(i, getXPixel(i, data), graph.height - yPadding + 20);
    }

    // Draw the Y value texts
    c.textAlign = "right"
    c.textBaseline = "middle";

    for (var i = 0; i < getMaxY(data) ; i += 10) {
        c.fillText(i, xPadding - 10, getYPixel(i, data));
    }

    c.strokeStyle = '#f00';

    // Draw the line graph
    c.beginPath();
    c.moveTo(getXPixel(data.values[0].X, data), getYPixel(data.values[0].Y, data));
    for (var i = 1; i < data.values.length; i++) {
        c.lineTo(getXPixel(data.values[i].X, data), getYPixel(data.values[i].Y, data));
    }
    c.stroke();

    // Draw the dots
    c.fillStyle = '#333';

    for (var i = 0; i < data.values.length; i++) {
        c.beginPath();
        c.arc(getXPixel(data.values[i].X, data), getYPixel(data.values[i].Y, data), 4, 0, Math.PI * 2, true);
        c.fill();
    }
}

function drawgraph(data, xLabel, yLabel, additionalString) {

    var containerDiv = document.getElementById("results_container");
    var resultDiv = document.createElement('div');
    $(resultDiv).addClass("result-container");
    graph = document.createElement('canvas');
    $(graph).addClass("canvas-graph");
    tipCanvas = document.createElement('canvas');
    containerDiv.appendChild(resultDiv);

    var yLabelObj = document.createElement("label")

    yLabelObj.appendChild(document.createTextNode(yLabel));
    $(yLabelObj).addClass("yLabel");

    resultDiv.appendChild(yLabelObj);

    resultDiv.appendChild(graph);
    resultDiv.appendChild(tipCanvas);

    var xLabelObj = document.createElement("label")
    xLabelObj.appendChild(document.createTextNode(xLabel));
    $(xLabelObj).addClass('xLabel');
    resultDiv.appendChild(xLabelObj);



    var offsetX = graph.offsetLeft;
    var offsetY = graph.offsetHeight;

    //var c = graph.getContext('2d');
    var graphValues = data.values;

    drawResults(graph, tipCanvas, data, xLabel, yLabel);
}

function clear() {
    $("#results_container").html("");
    ///$('#results_container').clear();
}