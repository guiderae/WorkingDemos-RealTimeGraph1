# WorkingDemos-RealTimeGraph1

This demo shows how to create a simple Flask web application that maintains a real time graph from data artificially generated to simulate real time data generation.  In particular the demo shows how to "push" data from a server side data source to the browser where a graph is updated each time a new data point is made available.  

The server side code is written in Python 3.8 and the client browser code is written in pure HTML5 and Javascript.  The Javascript library, plotly.js is used to render the graph on the browser.

The web framework used is Flask 2.0.1.

Make sure you have a path set to your Python interpreter.

In order to start the Flask server, cd to the folder WorkingDemos-RealTimeGraph1

Then run the server
  python wsgi.py
  
You will see in the console:

* Serving Flask app "wsgi" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 280-880-487

Notice that the response in the console shows a url of your web application:

http://127.0.0.1:5001

If you then enter this url into your browser, you will see the opening page of the web application.
