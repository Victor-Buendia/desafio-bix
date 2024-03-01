from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from scripts.ingest import main

with DAG(
    dag_id="ingestao-vendas",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    description="Realiza a ingestão dos dados das vendas, funcionários e categorias.",
    schedule='*/1 * * * *',
    start_date=datetime(2024,3,1),
    catchup=False,
    tags=["bix"],
) as dag:
	@task(task_id="daily_batch_ingestion")
	def ingest():
		result = main()

	daily_batch_ingestion
	