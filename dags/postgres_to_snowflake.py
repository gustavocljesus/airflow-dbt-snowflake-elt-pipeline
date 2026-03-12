from datetime import datetime, timedelta, timezone
from airflow.decorators import dag, task
from src.loaders.snowflake_load import load_incremental_data
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
    
    @task(task_id = 'get_last_date')
    def get_last_date(table_name: str):
        get_last_date_ingestion(table_name)
          
    @task(task_id = 'load_data_tables')
    def load(table_name, max_id):
        load_incremental_data(table_name, max_id)

    @task(task_id = 'update_control_table')
    def update_control_table(table_name: str):
        update_date_ingestion(table_name)
          
    for table_name in table_names:
        last_date = get_last_date(table_name)
        load(table_name, last_date)
        update_control_table(table_name)

postgres_to_snowflake_elt_dag = postgres_to_snowflake_elt()