# Web Log Parser

A web log parser using Flask and Python!

## Description

This is a web app that uses a default access log to parse. Users do have the option to import new log files and specify which file they want to parse. 

Users are able to see different default information about the log they chose with built in parameters, such as HTTP Status codes, unique IP counts, and others!

There is also API endpoints included that can be used to feed information into other programs. 

## Features

* View Unique IPs Count
* How Many Requests per IP	
* HTTP Status Code Distribution	
* Webpage Popularity
* Popular Browsers
* Request Method Distribution
* API List

## Getting Started

### Dependencies
* Python 3.x
* Flask
* Import os
* Browser to display web front end.

### Installing


Clone this repository as is.
```
mkdir webapp
cd webapp
git clone https://github.com/javainsmith/2KWebApp/
pip install Flask
```

### Executing program

* How to run the program:
* For Windows, I recommend running this program through PyCharm if available as it abstracts a lot of the customizations that’s needed to run python applications.
* For Mac/UNIX:
```
cd webapp
./app.py
```

This application will run on: http://localhost:5000/ by default.


## Authors

Author contact info

Javain Smith

## Version History

* 0.1
    * Initial Release
