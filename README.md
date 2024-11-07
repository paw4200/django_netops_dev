# README

## How do I get set up?

### Install Dependencies

```
sudo apt install apache2 apache2-utils ssl-cert libapache2-mod-wsgi-py3 -y

sudo apt install python3-django -y

sudo apt install mysql-server -y

sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config libssl-dev mysql-client

pip3 install mysqlclient

pip3 install django-bootstrap-v5

pip3 install django-import-export

pip3 install django-crispy-forms

pip3 install crispy-bootstrap5

pip3 install pydot

pip3 install networkx
```

### Database configuration

```
sudo mysql

CREATE DATABASE netopsdb;
CREATE USER 'dbadmin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'dbadmin'@'localhost';
FLUSH PRIVILEGES;
```

### Static and Migrate

```
cd netops/

python3 manage.py collectstatic

python3 manage.py makemigrations

python3 manage.py migrate
```
