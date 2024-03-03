from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import timedelta,datetime
from airflow.decorators import dag, task
import airflow

import sys
sys.path.append("/opt/airflow/plugins/")
sys.path.append("/opt/airflow/plugins/scripts")
from scripts.ingest import main

with DAG(
	dag_id="ingestao-vendas",
	default_args={
		"depends_on_past": False,
		"retries": 1,
		"retry_delay": timedelta(minutes=1),
	},
	description="Realiza a ingestão dos dados das vendas, funcionários e categorias.",
	schedule='0 0 * * *',
	start_date=datetime(2024,3,1),
	catchup=False,
	tags=["bix"],
) as dag:

	# @task(task_id="print_the_context")
	# def print_context(ds=None, **kwargs):
	# 	"""Print the Airflow context and ds variable from the context."""
	# 	pprint(kwargs)
	# 	print(ds)
	# 	return "Whatever you return gets printed in the logs"

	# run_this = print_context()

	# @task(task_id="paths")
	# def get_my_function():
	# 	import sys

	# 	print("Python Executable Path:", sys.executable)
	# 	print("Python Version:", sys.version)
	# 	print("sys.path:", sys.path)

	# 	from scripts.ingest import main

	# paths

	# config_env = BashOperator(
	# 	task_id="config_env",
	# 	bash_command="cd /opt/airflow/plugins && pip install -r requirements.txt",
	# )

	@task(task_id="daily_batch_ingestion")
	def ingest():
		main()

	daily_batch_ingestion = ingest()

	daily_batch_ingestion
	