# cloud_sql_and_cloud_run


<br>

# gcloud commandas

gcloud sql instances describe postgres-1

gcloud sql connect postgres-1 --database=cloudrun --user=sqluser

gcloud sql databases create cloudrun --instance="postgres-1"

gcloud sql connect postgres-1 --database=cloudrun --user=sqluser


# private IP - VM

sudo apt-get install postgresql-client

SELECT datname FROM pg_database;

see table \dt


psql "host=10.117.240.9 port=5432 sslmode=disable dbname=cloudrun user=sqluser"

