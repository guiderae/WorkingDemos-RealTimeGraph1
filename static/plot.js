var graph = document.getElementById("predGraph");
let data = [
    { // 0 Trace for Data points for sensor
        x: [],
        y: [],
        mode: 'line',
        marker: {color: 'red', size: 3},
        xaxis:{type: 'date'}
    },
    { // 1 Trace for Data points for sensor
        x: [],
        y: [],
        mode: 'line',
        marker: {color: 'green', size: 3},
        xaxis:{type: 'date'}
    },
    { // 2 Trace for Data points for sensor
        x: [],
        y: [],
        mode: 'line',
        marker: {color: 'blue', size: 3},
        xaxis:{type: 'date'}
    }];


// This array of empty traces is used whenever we need to restart a plot after it has been stopped.
// Since the array is empty, the restarted plot will start with no data.

let initData = [
    { // Trace0 for Data points for sensor
        x: [],
        y: [],
        mode: 'line',
        marker: {color: 'red', size: 3},
        xaxis:{type: 'date'}
    },
    { // Trace1 for Data points for sensor
        x: [],
        y: [],
        mode: 'line',
        marker: {color: 'green', size: 3},
        xaxis:{type: 'date'}
    },
    { // 2 Trace for Data points for sensor
        x: [],
        y: [],
        mode: 'line',
        marker: {color: 'blue', size: 3},
        xaxis:{type: 'date'}
    }];
    let layout = {
        title: {text: 'Failure Prediction',
                font: {size: 20},
                xanchor: 'center',
                yanchor: 'top'},
        margin: {t:50},
        xaxis: {type: 'date'},
        yaxis: {range: [0, 1],
                title: 'Scaled Sensors',
                side: 'left'},

        showlegend: true

    };

// First do a deep clone of the data array of traces.  The clone uses values from the empty array, initData
// Then call Plotly.newPlot() using the cloned array of empty traces to start a new plot.
function initPlot(){
    data[0].x = Array.from(initData[0].x);
    data[0].y = Array.from(initData[0].y);
    data[1].x = Array.from(initData[1].x);
    data[1].y = Array.from(initData[1].y);
    data[2].x = Array.from(initData[2].x);
    data[2].y = Array.from(initData[2].y);

    Plotly.newPlot('predGraph', data, layout);
}

var msgCounter = 0; // Another way of shifting. Not used in this code.

function updatePlot(jsonData){
    //console.log("plot.js updatePlot()  " + jsonData);
    let max = 120;
    let jsonObj = JSON.parse(jsonData);

    // Unpack json, keys are:
    //['timestamp', 'sensor_04', 'sensor_18', 'sensor_34']
    let timestamp = jsonObj.timestamp;
    let y1 =        jsonObj.sensor_04;
    let y2 =        jsonObj.sensor_18;
    let y3 =        jsonObj.sensor_34;
    // Note there are three traces.
    Plotly.extendTraces('predGraph',
        {
        x: [[timestamp], [timestamp], [timestamp]],
        y: [[y1], [y2], [y3]]

        }, [0, 1, 2], max);  // The array denotes to plot all three traces(0 based).  Keep only last max data points


}