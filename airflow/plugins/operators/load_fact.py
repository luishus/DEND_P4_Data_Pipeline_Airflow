from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlQueries

import logging

class LoadFactOperator(BaseOperator):
    
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table = "",
                 sql = "",        
                 *args, **kwargs):
                    
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)      
        logging.info("Insert data from staging tables into {} fact table".format(self.table))
        insert_sql = """
            INSERT INTO {table}
            {select_sql};
        """.format(table=self.table, select_sql=self.sql)        
        redshift.run(insert_sql)