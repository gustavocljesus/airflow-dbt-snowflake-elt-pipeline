from airflow.providers.standard.operators.bash import BashOperator

def transformation():
    return BashOperator(task_id="dbt_build",
                        bash_command="cd /opt/airflow/dags/dbt && dbt deps --profiles-dir /opt/airflow/dags/dbt && dbt build --profiles-dir /opt/airflow/dags/dbt")