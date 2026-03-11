from datetime import datetime, timedelta, timezone
from airflow.decorators import dag, task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from src.loaders.snowflake_load import load_incremental_data

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
    def get_last_date_ingestion(table_name: str):
        hook = SnowflakeHook(snowflake_conn_id = 'snowflake').get_conn()
            
        with hook as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT ultima_carga FROM controle_ingestao WHERE tabela = '{table_name}'")
                last_date = cursor.fetchone()[0]
                return last_date if last_date is not None else datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        
    @task(task_id = 'load_data_tables')
    def load(table_name, max_id):
        load_incremental_data(table_name, max_id)

    @task(task_id = 'update_control_table')
    def update_date_ingestion(table_name: str):
        hook = SnowflakeHook(snowflake_conn_id = 'snowflake').get_conn()

        with hook as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                MERGE INTO controle_ingestao AS ci
                USING (SELECT '{table_name}' AS tabela) src
                ON ci.tabela = src.tabela
                WHEN MATCHED THEN 
                    UPDATE SET ci.ultima_carga = CURRENT_TIMESTAMP
                WHEN NOT MATCHED THEN 
                    INSERT (tabela, ultima_carga) 
                    VALUES ('{table_name}', CURRENT_TIMESTAMP)
            """)
    
    for table_name in table_names:
        last_date = get_last_date_ingestion(table_name)
        load(table_name, last_date)
        update_date_ingestion(table_name)

postgres_to_snowflake_elt_dag = postgres_to_snowflake_elt()