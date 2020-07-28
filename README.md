# Project 5: Data Pipelines with Airflow

## Summary

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.


## Files in the repository

* **[airflow](airflow)**: workspace folder storing the airflow DAGs and plugins used by the airflow server.
* **[airflow/dags/udac_example_dag.py](airflow/dags/udac_example_dag.py)**: "Main"-DAG written in Python containing all steps of the pipeline.
* **[airflow/plugins/operators/](airflow/plugins/operators)**: Folder containing such called operators which can be called inside an Airflow DAG. These are python classes to outsource and build generic functions as modules of the DAG.

## The required DAG

<img src="./images/airflow_dag.JPG?raw=true" width="800" />


## Schema design and ETL pipeline

The star schema has 1 *fact* table (songplays), and 4 *dimension* tables (users, songs, artists, time).