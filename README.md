# LUCAS PIRES DE SOUZA

## Docker compose Running
Make sure if you have Docker application Running locally.

Run:
```bash
docker-compose up --build
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Local Running

### Prerequisites

    1. Python 3.x
    2. MySQL database

Go to app (.posterr\app) folder.

Install requirements:

```bash
pip install -r requirements.txt
```

you can run flask migration to create table

```bash
flask db init
flask db migrate
flask db upgrade
```
or run the db/init-scripts/ddl.sql to create table


Run application

```bash
python app.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Configuration

Located under the yaml file.

- **SQLALCHEMY_DATABASE_URI** MySQL db connection url

the config value can be set through environment variable **SQLALCHEMY_DATABASE_URI**.



or override with environment variable

```bash
SQLALCHEMY_DATABASE_URI=xxx python app.py
```



<br />

## Test and Verification

Import the postman collection in docs folder to test and verify.

<br />

# Critique
- Add automated tests the whole application instead of testing only via Postman
- 
