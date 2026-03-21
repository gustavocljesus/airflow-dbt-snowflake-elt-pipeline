from airflow.providers.standard.operators.bash import BashOperator

def transformation():
    return BashOperator(task_id="dbt_run",
                        bash_command="cd ~/airflow/dags/dbt && dbt run && dbt test --profiles-dir ~/airflow/dags/dbt")