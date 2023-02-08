# imperium

ImperiumBid - An Online Bidding Platform

## Requirements

- Python (> 3.8)
- PostgreSQL

## Running Instructions

- `cd imperium`
- `python -m venv venv`
- `. venv/Scripts/activate` (For Windows)
- `source venv/Scripts/activate` (For Git Bash)
- `source venv/bin/activate` (For Unix)
- `pip install -r requirements.txt`
- `cp web/core/.env.example web/core/.env`

Then configure PostgreSQL, and add all the environment variables in `web/.env`.

Finally run,

- `cd web`
- `python manage.py runserver`

To load dummy data,
- `cd web`
- `python manage.py loaddata dump.json`