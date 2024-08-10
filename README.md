# Chat API
This is an example API for a chat application made during my third semester at RIT as course project. All code that has been provided for the course has been replaced with alternatives.

## Requirements
Python requirements are listed within `requirements.txt`. Use `pip install -r ./requirements.txt` to install all dependencies.

This API also requires a running instance of PostgreSQL with a user and database owned by said user to be used by the server.

## Configuration
Configuration is handled in a single file located in `./config/db.yml`, which provides information on the PostgreSQL instance to connect to. Setup of the 