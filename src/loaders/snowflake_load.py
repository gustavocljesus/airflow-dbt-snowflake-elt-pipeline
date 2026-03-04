from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from ingestion.postgres_extractor import extract_data_postgres

def load_incremental_data(table_name: str, max_id: int):
    hook = SnowflakeHook(snowflake_conn_id = 'snowflake').get_conn()
    data, columns, placeholders = extract_data_postgres(table_name, max_id)
    
    with hook as sf_conn:
        with sf_conn.cursor() as sf_cursor:
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            for values in data:
                sf_cursor.execute(insert_query, values)
                        