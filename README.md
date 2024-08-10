# Chat API
This is an example API for a chat application made during my third semester at RIT as course project. All code that has been provided for the course has been replaced with alternatives.

## Requirements
This requires Python 3.12.5 to run as well as `pip`.
Python requirements are listed within `requirements.txt`. Use `pip install -r ./requirements.txt` to install all dependencies.

### Arch Linux Users
Arch Linux discourages the usage of `pip` and urges the use of `pacman` for installing python modules. The command to install all dependencies is 
```bash
sudo pacman -S python-{aniso8601,atomicwrites,attrs,certifi,
charset-normalizer,click,colorama,flask{-restful},idna,
importlib-metadata,iniconfig,itsdangerous,jinja,markupsafe,
more-itertools,packaging,pluggy,psycopg{-pool},py,pyparsing,pytest,
pytz,pyyaml,requests,six,tomli,urllib3,wcwidth,werkzeug,zipp}
```

This API also requires a running instance of PostgreSQL (tested with v16.3) with a user and database owned by said user to be used by the server.

## Configuration
Configuration is handled in a single file located in `./config/db.yml`, which provides information on an existing PostgreSQL database to connect to.

## Running
In order to run the server execute `python src/server.py` with no arguments. 

### Testing
In order to run tests on the server you must have the server running first (using command above). When the server is running execute `pytest` to run the tests.