// This script first creates listeners for the start and stop buttons.
// It also creates an EventSource that is linked to the url,
// '/runPredict'. Once instantiated, theEventSource establishes a
// permanent socket that only allows server push communication.  In this
// application there are two event messages that are pushed to the
// browser: 'update', and 'jobfinished'.  There is also a listener for
// 'initialize', but it is not needed in this application.
const startPlotBtn = document.getElementById("startPredictBtn");
const stopPlotBtn = document.getElementById("stopPredictBtn");
const predictCSVNameObj = document.getElementById("predictCSV");
startPlotBtn.addEventListener('click', startPlotProcess);
stopPlotBtn.addEventListener('click', stopPlotProcess);

let eventSourceGraph;
function startPlotProcess(){
    // Get the data source file name from the UI
    let predictCSVName =
        predictCSVNameObj.options[predictCSVNameObj.selectedIndex].text;
    const url = "/runPredict?" + "predictCSVFileName=" + predictCSVName;
    initPlot();
    if(eventSourceGraph){
        eventSourceGraph.close();
    }
    // Create a JS EventSource object and give it the URL of a long
    // running task.  The EventSource object keeps the connection open
    // to the given URL so that the process at the end point
    // can send messages
    // back to the EventSource object.
    eventSourceGraph = new EventSource(url);
    // NOTE:  This event 'initialize' is currently not used
    eventSourceGraph.addEventListener("initialize",
                                function(event){
        initPlot();
    }, false);
    // "update" Event contains the plotting data
    eventSourceGraph.addEventListener("update",
                                function(event){
        updatePlot(event.data);

    }, false);
    // "jobfinished" Event gets back finished message generated by the
    // server when the data source is exhausted
    eventSourceGraph.addEventListener("jobfinished",
                                function(event){
        eventSourceGraph.close();
        startPlotBtn.disabled = false;
    }, false);
    startPlotBtn.disabled = true;  // Disable start btn after plot is started.
}
// Closes the EventSource object which closes the connection between
// browser and server.
function stopPlotProcess(){
    console.log("Stopping process");
    eventSourceGraph.close();
    startPlotBtn.disabled = false;  // Enable start btn after process
    // is terminated.
}