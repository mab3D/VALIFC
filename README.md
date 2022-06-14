# VALIFC PROJECT
The current project contains a site
In which an ifc file can be uploaded and validated on the existence of space and metadata. Note that it might only work on a local server.

## SETUP
**dependancies**:
  + Python 3 or higher
  + Python libs:
    - Venv
    - ifcopenshell



  **Set Paths**:
    + In _Init_.py change the location of the upload folder and the postgres database connection

## IMPORTANT RESOURCES
+ The project uses flaksr, for documentation on flaskr see:
https://www.google.com/search?client=firefox-b-d&q=flaskr

+ The project uses the ifcopenshell library, see:
http://ifcopenshell.org/

Could be interesting to look at, I could not get it to work,
but this might include a viewer compatible with ifcopenshell
https://dev.opencascade.org/release
git://github.com/tpaviot/pythonocc-core.git

## START
The following actions are commands in CMD

Go to the location of the flaskr folder

```
cd ../../Flask1
```

Activate the virtual environment
```
venv\Scripts\activate
```

Set Flask parameters
```
set FLASK_APP=flaskr
set FLASK_ENV=development
```

Iniate the database (only needed once, or if you want to reset the database)
```
flask init-db
```

Start flask
```
flask run
```

A location appears were flask is running. Usually somewhere local like 127.0.0.1:5000
Enter this location in a web browser.
The application is now running.
It will echo the actions in the CMD
Since dev mode is on, you can change the scripts while Flask is running
