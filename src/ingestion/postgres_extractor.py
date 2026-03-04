from airflow.providers.postgres.hooks.postgres import PostgresHook

def extract_data_postgres(table_name: str, max_id: int):
    hook = PostgresHook(postgres_conn_id = 'postgres').get_conn()

    with hook as pg_conn: 
        with pg_conn.cursor() as pg_cursor:
            primary_key = f'id_{table_name}'

            pg_cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            columns = [row[0] for row in pg_cursor.fetchall()]
            columns_list = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))

            pg_cursor.execute(f"SELECT {columns_list} FROM {table_name} WHERE {primary_key} > {max_id}")
            rows = pg_cursor.fetchall()

            return rows, columns_list, placeholders