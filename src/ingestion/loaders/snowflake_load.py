import logging
from common.decorators import measure_time
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from src.ingestion.extract.postgres_extractor import extract_data_postgres

logger = logging.getLogger(__name__)

@measure_time("load")
def load_incremental_data(table_name: str, last_date: str):
    logger.info("event=load_start target=snowflake table=%s last_date=%s",
                table_name,
                last_date)
    
    try: 
        hook = SnowflakeHook(snowflake_conn_id = 'snowflake').get_conn()
        data, columns, placeholders = extract_data_postgres(table_name, last_date)
        
        with hook as sf_conn:
            with sf_conn.cursor() as sf_cursor:
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                # evitar carga incompleta dos dados devido a alguma interrupcao
                try:
                    sf_conn.autocommit = False
                    for values in data:
                        sf_cursor.execute(insert_query, values)
                    sf_conn.commit()
                except Exception as e:
                    sf_conn.rollback()
                    raise # relanca o erro para o airflow marcar a task como falha
        
        logger.info("event=load_finish target=snowflake table=%s rows_inserted=%s",
                    table_name,
                    len(data))
    
    except Exception:
        logger.exception("event=load_error target=snowflake table=%s",
                         table_name)
        raise
                        