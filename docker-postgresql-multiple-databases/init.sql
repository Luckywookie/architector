CREATE USER auth_user;
ALTER USER auth_user WITH PASSWORD 'pwd0123456789';
CREATE DATABASE sanic_postgres__auth;
GRANT ALL PRIVILEGES ON DATABASE sanic_postgres__auth TO auth_user;

CREATE USER catalog_user;
ALTER USER catalog_user WITH PASSWORD 'pwd__catalog_0123456789';
CREATE DATABASE sanic_postgres__catalog;
GRANT ALL PRIVILEGES ON DATABASE sanic_postgres__catalog TO catalog_user;