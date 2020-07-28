from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

import logging

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 tables = {},
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables
        

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)  
        tables = self.tables.keys()
        primary_keys = self.tables.values()
        for table in tables:
            records = redshift.get_records("SELECT COUNT(*) FROM {}".format(table))        
            if len(records) < 1 or len(records[0]) < 1:
                logging.error("{} returned no results".format(table))
                raise ValueError("Data quality check failed. {} returned no results".format(table))
            num_records = records[0][0]
            if num_records == 0:
                logging.error("No records present in destination table {}".format(table))
                raise ValueError("No records present in destination {}".format(table))
            logging.info("Data quality on table {} check passed with {} records".format(table, num_records))  
                                
            null_records = redshift.get_records("SELECT COUNT(*) FROM {} WHERE {} IS NULL".format(table,self.tables.get(table)))
            num_records = null_records[0][0]
            if num_records >= 1:
                logging.error("{} field from {} table returned {} null values".format(self.tables.get(table),table,num_records))
                raise ValueError("Data quality check failed. {} field from {} table returned {} null values".format(self.tables.get(table),table,num_records))
            if num_records == 0:
                logging.info("Data quality on field {} from {} table check passed without null values".format(self.tables.get(table), table))               
            
            
            