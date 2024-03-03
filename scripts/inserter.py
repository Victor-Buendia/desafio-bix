from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.dialects.sqlite import insert

class Inserter():
	def __init__(self):
		pass

	def insert_data_into_psql(self,database,source_data,Table,primary_key):
		data = source_data
		try:
			insert_stmt = insert(Table).values(data)
			insert_stmt = insert_stmt.on_conflict_do_update(
				index_elements=[primary_key],
				set_=dict(insert_stmt.excluded)
			)
			database.session.execute(insert_stmt)
			database.session.commit()
		except (IntegrityError, OperationalError) as e:
			print(f"Error: {e}")