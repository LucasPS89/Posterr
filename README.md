# LUCAS PIRES DE SOUZA

<br />
<br />

# Running the application
## Docker compose Running
Make sure if you have Docker application Running locally.

Run:
```bash
docker-compose up --build
```
<br />

## Local Running
<br />

### Prerequisites

    1. Python 3.x
    2. MySQL database

## Configuration

Create a Database named Posterr in your MySqlServer;

Located the file app/config.yaml and adjust to point to your MySql server:

- SQLALCHEMY_DATABASE_URI: 'mysql+pymysql://myuser:mypassword@localhost:3306/posterr?charset=utf8mb4'

<br />

## Steps

Go to app (.posterr\app) folder.

Install requirements:

```bash
pip install -r requirements.txt
```

you can run flask migration to create table or you can run the script db/init-scripts/ddl.sql 

```bash
flask db init
flask db migrate
flask db upgrade
```

<br />
On the App folder, Run application via

```bash
python app.py
```





<br />

# Test and Verification

Import the Postman collection in docs folder to test and verify. You can run the requests in the same order they are saved as they are presented in the same order as the STA.

<br />

# Critique
- Add automated tests the whole application instead of testing only via Postman;
- Although SqlAlchemy makes it easier to manipulate data, it's not the best option for high performance;
