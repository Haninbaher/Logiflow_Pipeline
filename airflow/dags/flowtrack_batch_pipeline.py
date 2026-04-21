from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "flowtrack",
    "depends_on_past": False,
}

with DAG(
    dag_id="flowtrack_batch_pipeline",
    default_args=default_args,
    description="FlowTrack batch and modeling pipeline",
    start_date=datetime(2026, 4, 21),
    schedule_interval=None,
    catchup=False,
    tags=["flowtrack", "batch", "dbt"],
) as dag:

    ingest_static_data = BashOperator(
        task_id="ingest_static_data",
        bash_command=(
            "docker exec flowtrack_spark "
            "python3 /opt/spark/work-dir/jobs/batch/ingest_static_data.py"
        ),
    )

    transform_static_data = BashOperator(
        task_id="transform_static_data",
        bash_command=(
            "docker exec flowtrack_spark "
            "python3 /opt/spark/work-dir/jobs/batch/transform_static_data.py"
        ),
    )

    transform_shipment_events = BashOperator(
        task_id="transform_shipment_events",
        bash_command=(
            "docker exec flowtrack_spark "
            "python3 /opt/spark/work-dir/jobs/batch/transform_shipment_events.py"
        ),
    )

    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command=(
            "docker exec flowtrack_dbt "
            "dbt run --profiles-dir /usr/app"
        ),
    )

    ingest_static_data >> transform_static_data >> transform_shipment_events >> run_dbt_models
