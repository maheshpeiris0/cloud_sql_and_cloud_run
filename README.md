# cloud_sql_and_cloud_run


<br>

# gcloud commands

gcloud sql instances describe postgres-1

gcloud sql users create sqluser --instance=postgres-1 --password="canada"

gcloud sql databases create cloudrun --instance="postgres-1"

gcloud sql connect postgres-1 --database=cloudrun --user=sqluser


# private IP - VM

sudo apt-get install postgresql-client

SELECT datname FROM pg_database;

see table \dt


psql "host=10.117.240.9 port=5432 sslmode=disable dbname=cloudrun user=sqluser"

CREATE TABLE IF NOT EXISTS employee ( name VARCHAR(255) NOT NULL, age INT NOT NULL, country VARCHAR(255) NOT NULL );
