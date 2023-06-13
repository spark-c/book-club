# Project Setup

Temporary reference for starting the project in a new environment. Database steps may or may not have correct commands...

## Init environment

1. Install psql / postgres
    1. `CREATE USER bookclub;`
    1. `CREATE DATABASE bookclubdb;`
    1. `ALTER DATABASE bookclubdb OWNER TO bookclub;`
    1. `ALTER ROLE bookclub WITH CREATEDB;`
1. Check that the scripts `(win)startdb` and `(win)stopdb` work. You may need to update them to correctly point to your postgres installation.
1. Create venv: `python3 -m venv .venv`
1. Install requirements: `python3 -m pip install -r requirements.txt`
1. Check that pytest is able to find and run tests: `pytest`
1. You can check for errors with: `python3 manage.py check`
1. Create database migrations: `python3 manage.py createmigrations`
1. Migrate db: `python3 manage.py migrate`

## Start development server

1. Make sure postgres server is running: `bash startdb.sh` or `./winstartdb.ps1`
1. Start dev server: `python3 manage.py runserver`
