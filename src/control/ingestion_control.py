from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime, timezone

def get_last_date_ingestion(table_name: str):
        hook = SnowflakeHook(snowflake_conn_id = 'snowflake').get_conn()
            
        with hook as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT ultima_carga FROM controle_ingestao WHERE tabela = '{table_name}'")
                last_date = cursor.fetchone()[0]
                return last_date if last_date is not None else datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

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