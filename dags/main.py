from airflow import DAG
import pendulum
from datetime import datetime,timedelta
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
# from pydantic._internal import _schema_gather

from api.video_stats import get_playlist_id,extract_video_data,save_to_json
from api.video_stats import get_video_ids
# from dags.dataquality.soda import yt_elt_data_quality

from datawarehouse.dwh import staging_table,core_table
from dataquality.soda import yt_elt_data_quality

#define local timezone

locat_tz = pendulum.timezone("Asia/Shanghai")

# defaults args

default_args = {
    'owner': 'dataengineers',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    #retry delay
    'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
    'dagrun_timeout': timedelta(hours=1),
    'start_date': datetime(2026, 1, 1, tzinfo=locat_tz),
    # 'end_date': datetime(2030, 1, 1, tzinfo=locat_tz),
}

#variables
staging_schema = "staging"
core_schema = "core"


# DAG 1: produce_json
with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='DAG to produce JSON with raw data',
    schedule_interval='0 14 * * *',
    catchup=False,

) as dag_produce:

    #define task
    playlist_id=get_playlist_id()
    video_id=get_video_ids(playlist_id)
    extract_data=extract_video_data(video_id)
    save_to_json_task=save_to_json(extract_data)

    trigger_update_db = TriggerDagRunOperator(
        task_id="trigger_update_db",
        trigger_dag_id="update_db",
    )

    # define dependancies
    playlist_id >> video_id >> extract_data >> save_to_json_task >> trigger_update_db

# DAG 2: update_db
with DAG(
    dag_id='update_db',
    default_args=default_args,
    description='DAG to process JSON file and insert data into staging and core shcmea',

    catchup=False,
    schedule=None,

) as dag_update:

    #define task
    update_staging = staging_table()
    update_core = core_table()

    trigger_data_quality = TriggerDagRunOperator(
        task_id="trigger_data_quality",
        trigger_dag_id="data_quality",
    )

    # define dependancies

    update_staging >> update_core >> trigger_data_quality

# DAG 3: data_quality
with DAG(
    dag_id='data_quality',
    default_args=default_args,
    description='DAG to check data quality on both layers in database',

    catchup=False,
    schedule=None,

) as dag_quality:

    #define task
    soda_validate_staging = yt_elt_data_quality(staging_schema)
    soda_validate_core = yt_elt_data_quality(core_schema)

    # update_staging = staging_table()
    # update_core = core_table()
    # define dependancies

    soda_validate_staging >> soda_validate_core
