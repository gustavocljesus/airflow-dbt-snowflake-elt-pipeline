from airflow.providers.standard.operators.bash import BashOperator

def transformation():
    return BashOperator(task_id="dbt_build",
                        bash_command="cd ~/airflow/dags/dbt && dbt build --profiles-dir ~/airflow/dags/dbt")