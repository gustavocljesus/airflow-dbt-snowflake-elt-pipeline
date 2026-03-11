from airflow.providers.postgres.hooks.postgres import PostgresHook

def extract_data_postgres(table_name: str, last_date: str):
    hook = PostgresHook(postgres_conn_id = 'postgres').get_conn()

    with hook as pg_conn: 
        with pg_conn.cursor() as pg_cursor:

            pg_cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            columns = [row[0] for row in pg_cursor.fetchall()]
            columns_list = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))

            pg_cursor.execute(f"SELECT {columns_list} FROM {table_name} WHERE data_inclusao >= {last_date}")
            rows = pg_cursor.fetchall()

            return rows, columns_list, placeholders