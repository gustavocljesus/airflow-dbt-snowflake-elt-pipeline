from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from src.loaders.snowflake_load import load_incremental_data

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'start_date' : datetime(2024,1,1),
    'email_on_failure' : False,
    'email_on_retry': False,
    'retries' : 0,
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
    
    @task(task_id = 'get_max_id')
    def get_max_primary_key(table_name: str):
        hook = SnowflakeHook(snowflake_conn_id = 'snowflake').get_conn()
            
        with hook as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT MAX(id_{table_name}) FROM {table_name}')
                max_id = cursor.fetchone()[0]
                return max_id if max_id is not None else 0 
        
    @task(task_id = 'load_data_tables')
    def load(table_name, max_id):
        load_incremental_data(table_name, max_id)

        for table_name in table_names:
            max_id = get_max_primary_key(table_name)
            load(table_name, max_id)

postgres_to_snowflake_elt_dag = postgres_to_snowflake_elt()