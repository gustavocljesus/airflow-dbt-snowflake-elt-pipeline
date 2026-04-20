from datetime import datetime, timedelta
from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator
from src.ingestion.loaders.snowflake_load import load_incremental_data
from src.control.ingestion_control import get_last_date_ingestion, update_date_ingestion

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'start_date' : datetime(2026,1,1),
    'email_on_failure' : False,
    'email_on_retry': False,
    'retries' : 3,
    'retry_delay' : timedelta(minutes=5),
}

@dag(
    dag_id = 'postgres_to_snowflake',
    default_args = default_args,
    description = 'Load data incrementally from Postgres to Snowflake',
    schedule = timedelta(days = 1),
    catchup = False,
    max_active_runs = 1
)
def postgres_to_snowflake_elt():
    table_names = [
        'veiculos',
        'estados',
        'cidades',
        'concessionarias',
        'vendedores',
        'clientes',
        'vendas'
    ]
    
    all_done = []

    @task
    def get_last_date(table_name: str):
        return get_last_date_ingestion(table_name)
          
    @task
    def load(table_name, last_date):
        load_incremental_data(table_name, last_date)

    @task
    def update_control_table(table_name: str):
        update_date_ingestion(table_name)    
          
    for table_name in table_names:
        last_date = get_last_date.override(task_id=f"get_last_date_{table_name}")(table_name)
        loaded = load.override(task_id=f"load_{table_name}")(table_name, last_date)
        updated = update_control_table.override(task_id=f"update_control_table_{table_name}")(table_name)
        loaded >> updated
        all_done.append(updated)

    dbt_task = BashOperator(task_id="dbt_build",
                        bash_command="cd /opt/airflow/dags/dbt && dbt deps --profiles-dir /opt/airflow/dags/dbt && dbt build --profiles-dir /opt/airflow/dags/dbt")
    
    all_done >> dbt_task

postgres_to_snowflake_elt_dag = postgres_to_snowflake_elt()