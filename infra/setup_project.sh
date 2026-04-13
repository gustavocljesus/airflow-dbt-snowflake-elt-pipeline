#!/bin/bash
set -e

cd ~/airflow-dbt-snowflake-elt-pipeline

echo "Movendo arquivos..."

cp ./dags/postgres_to_snowflake.py ~/airflow/dags/
cp ./Dockerfile ~/airflow/
cp ./requirements.txt ~/airflow/

echo "Movendo pastas..."

cp -r ./src/ ~/airflow/dags/
cp -r ./dbt/ ~/airflow/dags/

echo "-------------------------------------"
echo "Airflow disponível em:"
echo "http://SEU_IP_PUBLICO:8080"
echo "-------------------------------------"