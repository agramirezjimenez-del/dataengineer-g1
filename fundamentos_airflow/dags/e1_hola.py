from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

@dag(
    schedule="@daily",
    start_date=datetime(2026,10,26),
    catchup=False,
    tags=["Ejercicio e1"]
)

def e1_hola():
    saludar = BashOperator(
        task_id="saludar",
        bash_command="echo 'Hola, Airflow!'"
    )
    
    fecha = BashOperator(
        task_id="fecha",
        bash_command="echo 'Procesado el dia {{ ds}}'"
    )
    
    despedir = BashOperator(
        task_id="despedir",
        bash_command="echo 'Fin de ejecución, dag-id: {{dag.dag_id}}'"
    )
    
    saludar >> fecha >> despedir

e1_hola()