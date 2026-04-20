import logging
from src.common.decorators import measure_time
from airflow.providers.postgres.hooks.postgres import PostgresHook

logger = logging.getLogger(__name__)

@measure_time("extract")
def extract_data_postgres(table_name: str, last_date: str):
    logger.info("event=extract_start source=postgres table=%s last_date=%s",
                table_name,
                last_date)
    
    try:
        hook = PostgresHook(postgres_conn_id = 'postgres').get_conn()

        with hook as pg_conn: 
            with pg_conn.cursor() as pg_cursor:

                pg_cursor.execute(f"""
                                SELECT column_name 
                                FROM information_schema.columns 
                                WHERE table_name = %s
                                """,
                                (table_name,))
                
                columns = [row[0] for row in pg_cursor.fetchall()]
                columns_list = ', '.join(columns)
                placeholders = ', '.join(['%s'] * len(columns))

                pg_cursor.execute(f"""
                                SELECT {columns_list} 
                                FROM {table_name} 
                                WHERE data_inclusao > %s
                                """,
                                (last_date,))
                
                rows = pg_cursor.fetchall()

                logger.info("event=extract_finish source=postgres table=%s rows=%s columns_count=%s",
                            table_name,
                            len(rows),
                            len(columns))
                
                return rows, columns_list, placeholders
    
    except Exception:
        logger.exception("event=extract_error source=postgres table=%s",
                         table_name)
        raise