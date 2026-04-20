import logging
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def get_last_date_ingestion(table_name: str):
        logger.info("event=get_last_date_ingestion_start  table=%s", table_name)
        
        try:
            hook = SnowflakeHook(snowflake_conn_id = 'snowflake').get_conn()
                
            with hook as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                                SELECT ultima_carga 
                                FROM controle_ingestao 
                                WHERE tabela = %s 
                                """,
                                (table_name,))
                    
                    last_date = cursor.fetchone()

                    if last_date is not None:
                         logger.info("event=get_last_date_ingestion_finish table=%s date=%s", 
                                     table_name,
                                     last_date[0])
                         
                         return last_date[0]
                    else:
                         default = datetime(2024, 1, 1, tzinfo=timezone.utc)
                         logger.warning("event=get_last_date_ingestion_default table=%s date=%s", 
                                        table_name,
                                        default)
                         
                         return default
        
        except Exception:
             logger.exception("event=get_last_date_ingestion_error")
             raise

def update_date_ingestion(table_name: str):
        logger.info("event=update_date_ingestion_start table=%s", table_name)

        try:
            hook = SnowflakeHook(snowflake_conn_id = 'snowflake').get_conn()

            with hook as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""
                    MERGE INTO controle_ingestao AS ci
                    USING (SELECT %s AS tabela) src
                    ON ci.tabela = src.tabela
                    WHEN MATCHED THEN 
                        UPDATE SET ultima_carga = CURRENT_TIMESTAMP
                    WHEN NOT MATCHED THEN 
                        INSERT (tabela, ultima_carga) 
                        VALUES (%s, CURRENT_TIMESTAMP)
                """,
                (table_name, table_name))
            
            logger.info("event=update_date_ingestion_finish table=%s", table_name)
        
        except Exception:
             logger.exception("event=update_date_ingestion_error table=%s", table_name)
             raise