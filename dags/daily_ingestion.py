from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import timedelta,datetime
from airflow.decorators import dag, task
import airflow
import os

from pipeline import Main
from environment import Environment

with DAG(
	dag_id="ingestao-vendas",
	default_args={
		"retries": 1,
		"depends_on_past": False,
		"retry_delay": timedelta(seconds=10),
	},
	description="Realiza a ingestão dos dados das vendas, funcionários e categorias.",
	schedule='0 0 * * *',
	start_date=datetime(2024,3,1),
	catchup=False,
	tags=["bix"],
) as dag:

	@task(task_id="check_env_variables")
	def check_env_vars(**kwargs):
		env = Environment()
		env.retrieve_env_variables()
		env.check_env_variables()

	@task(task_id="create_tables")
	def create_tables(**kwargs):
		main = Main()
		main.local_psql.create_tables()
		main.close_connection()

	@task(task_id="ingest_psql")
	def ingest_psql(**kwargs):
		main = Main()
		env = Environment()
		bix_psql = main.start(
			host=env.load_env('BIX_DB_HOST'),
			port=env.load_env('BIX_DB_PORT'),
			user=env.load_env('BIX_DB_USER'),
			pswd=env.load_env('BIX_DB_PASS'),
			db=env.load_env('BIX_DB_NAME')
		)
		main.ingest_vendas(db_from=bix_psql,db_to=main.local_psql)
		main.close_connection(bix_psql)
		main.close_connection()

	@task(task_id="ingest_api")
	def ingest_api(**kwargs):
		main = Main()
		main.ingest_funcionarios(db_to=main.local_psql)
		main.close_connection()

	@task(task_id="ingest_parquet")
	def ingest_parquet(**kwargs):
		main = Main()
		main.ingest_categorias(db_to=main.local_psql)
		main.close_connection()

	check_env_vars = check_env_vars()
	create_tables = create_tables()
	ingest_psql = ingest_psql()
	ingest_api = ingest_api()
	ingest_parquet = ingest_parquet()

	check_env_vars >>create_tables >> [ingest_psql, ingest_parquet, ingest_api]