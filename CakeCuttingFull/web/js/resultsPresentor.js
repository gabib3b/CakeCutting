/**
 * Created by gabib3b on 20/06/15.
 */


function startDrawing()
{
    var data = {
        values: [
            {X: 0, Y: 12},
            {X: 2, Y: 28},
            {X: 3, Y: 18},
            {X: 4, Y: 34},
            {X: 5, Y: 40},
            {X: 6, Y: 80},
            {X: 7, Y: 80}
        ]
    };

    drawgraph(data);
}


 function drawgraph(data, xLabel, yLabel, additionalString)
    {

   var graph;
   var xPadding = 30;
   var yPadding = 30;
    
     var containerDiv = document.getElementById("results_container");
     var resultDiv = document.createElement('div');
     
     var graphDetails = document.createElement("label");
     
     var labelVal = "X:"+ xLabel +" Y:" +yLabel;
     if(additionalString)
     {
         labelVal += ' ' + additionalString;
     }
     graphDetails.innerHTML = labelVal ;
     
     var graph = document.createElement('canvas');
     containerDiv.appendChild(resultDiv);  
     resultDiv.appendChild(graph);
    
    resultDiv.appendChild(graphDetails);


    function getMaxY() {
        var max = 0;

        for (var i = 0; i < data.values.length; i++) {
            if (data.values[i].Y > max) {
                max = data.values[i].Y;
            }
        }

        max += 10 - max % 10;
        return max;
    }

    function getMaxX() {
        var max = 0;

        for (var i = 0; i < data.values.length; i++) {
            if (data.values[i].X > max) {
                max = data.values[i].X;
            }
        }

        max += 10 - max % 10;
        return max;
    }

    function getXPixel(val) {
        // uses the getMaxX() function
        return ((graph.width - xPadding) / getMaxX()) * val + (xPadding * 1.5);
    }

    function getYPixel(val) {
        return graph.height - (((graph.height - yPadding) / getMaxY()) * val) - yPadding;
    }

    var c = graph.getContext('2d');

    c.lineWidth = 2;
    c.strokeStyle = '#333';
    c.font = 'italic 8pt sans-serif';
    c.textAlign = "center";

    c.beginPath();
    c.moveTo(xPadding, 0);
    c.lineTo(xPadding, graph.height - yPadding);
    c.lineTo(graph.width, graph.height - yPadding);
    c.stroke();

    for (var i = 0; i < data.values.length; i++) {
        // uses data.values[i].X
        c.fillText(data.values[i].X, getXPixel(data.values[i].X), graph.height - yPadding + 20);
    }

    c.textAlign = "right"
    c.textBaseline = "middle";

    for (var i = 0; i < getMaxY(); i += 10) {
        c.fillText(i, xPadding - 10, getYPixel(i));
    }

    c.strokeStyle = '#f00';

    c.beginPath();
    c.moveTo(getXPixel(data.values[0].X), getYPixel(data.values[0].Y));
    for (var i = 1; i < data.values.length; i++) {
        c.lineTo(getXPixel(data.values[i].X), getYPixel(data.values[i].Y));
    }
    c.stroke();

    c.fillStyle = '#333';

    for (var i = 0; i < data.values.length; i++) {
        c.beginPath();
        c.arc(getXPixel(data.values[i].X), getYPixel(data.values[i].Y), 4, 0, Math.PI * 2, true);
        c.fill();
    }
}


//    function drawgraph(data)
//    {
//
//       var containerDiv = document.getElementById("results_container");
//       var graph = document.createElement('canvas');
//       containerDiv.appendChild(graph);
//    
//
//    var graph;
//    var xPadding = 30;
//    var yPadding = 30;
//
//// Notice I changed The X values
//
//
//// Returns the max Y value in our data list
//    function getMaxY() {
//        var max = 0;
//
//        for (var i = 0; i < data.values.length; i++) {
//            if (data.values[i].Y > max) {
//                max = data.values[i].Y;
//            }
//        }
//
//        max += 10 - max % 10;
//        return max;
//    }
//
//// Returns the max X value in our data list
//    function getMaxX() {
//        var max = 0;
//
//        for (var i = 0; i < data.values.length; i++) {
//            if (data.values[i].X > max) {
//                max = data.values[i].X;
//            }
//        }
//
//        max += 10 - max % 10;
//        return max;
//    }
//
//// Return the x pixel for a graph point
//    function getXPixel(val) {
//        // uses the getMaxX() function
//        return ((graph.width - xPadding) / getMaxX()) * val + (xPadding * 1.5);
//    }
//
//// Return the y pixel for a graph point
//    function getYPixel(val) {
//        return graph.height - (((graph.height - yPadding) / getMaxY()) * val) - yPadding;
//    }
//
//    //graph = document.getElementById("graph");
//    var c = graph.getContext('2d');
//
//    c.lineWidth = 2;
//    c.strokeStyle = '#333';
//    c.font = 'italic 8pt sans-serif';
//    c.textAlign = "center";
//
//// Draw the axises
//    c.beginPath();
//    c.moveTo(xPadding, 0);
//    c.lineTo(xPadding, graph.height - yPadding);
//    c.lineTo(graph.width, graph.height - yPadding);
//    c.stroke();
//
//// Draw the X value texts
//    for (var i = 0; i < data.values.length; i++) {
//        // uses data.values[i].X
//        c.fillText(data.values[i].X, getXPixel(data.values[i].X), graph.height - yPadding + 20);
//    }
//
//// Draw the Y value texts
//    c.textAlign = "right"
//    c.textBaseline = "middle";
//
//    for (var i = 0; i < getMaxY(); i += 10) {
//        c.fillText(i, xPadding - 10, getYPixel(i));
//    }
//
//    c.strokeStyle = '#f00';
//
//// Draw the line graph
//    c.beginPath();
//    c.moveTo(getXPixel(data.values[0].X), getYPixel(data.values[0].Y));
//    for (var i = 1; i < data.values.length; i++) {
//        c.lineTo(getXPixel(data.values[i].X), getYPixel(data.values[i].Y));
//    }
//    c.stroke();
//
//// Draw the dots
//    c.fillStyle = '#333';
//
//    for (var i = 0; i < data.values.length; i++) {
//        c.beginPath();
//        c.arc(getXPixel(data.values[i].X), getYPixel(data.values[i].Y), 4, 0, Math.PI * 2, true);
//        c.fill();
//    }
//}