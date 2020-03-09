CREATE USER auth_user;
CREATE DATABASE sanic_postgres__auth;
GRANT ALL PRIVILEGES ON DATABASE sanic_postgres__auth TO auth_user;

CREATE USER catalog_user;
CREATE DATABASE sanic_postgres__catalog;
GRANT ALL PRIVILEGES ON DATABASE sanic_postgres__catalog TO catalog_user;