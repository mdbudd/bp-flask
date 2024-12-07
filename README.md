# Python/jMeter playground

A project that so far uses to Docker create a Jupyter server, a Flask API & significant setup of jMeter. It contains an automated framework to run *.jmx tests by name, plus the ability to run the GUI through a VNC so you can structure those tests.

## Python

Prep by copying `/python/flask/envfile.example.ini` to `/python/flask/envfile.ini` and configure accordingly. Base config will run.

To build the main python image and keep the container running by hosting a Flask API, run the following...
```
make compose
```
With the main Flask API running, run the following to piggyback that container and run the jupyter server. Once running, explore the data!
```
make jupyter
```

With the main Flask API running, run the following to piggyback that container and run unit tests on the Flask API etc...
```
make unit_test
```

## jMeter

Create a new jMeter image by running the following. This image is setup for automating tests internally...
```
make jmeter_build
```
Create the jMeter GUI image by running the following...
```
make jmeter_ui
```
To use the jMeter GUI, run the following...
```
make run_gui
```
...Once running you can use you favourite VNC viewer to connect to `localhost:5900` and structure your tests. They will appear in the project folders.

The following will run the corresponding `nameOfTest.jmx` file and generate the resulting dashboards to view results...
```
make jmeter_test NAME=nameOfTest
```

The following will run the corresponding `nameOfTest.jmx` file and generate the results, data only...
```
make non_gui NAME=nameOfTest
```