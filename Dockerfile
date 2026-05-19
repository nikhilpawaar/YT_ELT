ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

ENV AIRFLOW_HOME=/opt/airflow

USER root

COPY requirements.txt /

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -r /requirements.txt

# Create ALL required Airflow log folders
RUN mkdir -p \
    /opt/airflow/logs/scheduler \
    /opt/airflow/logs/dag_processor_manager \
    /opt/airflow/logs/dag_processor \
    /opt/airflow/logs/webserver \
    /opt/airflow/logs/worker \
    /opt/airflow/logs/triggerer

# Fix ownership
RUN chown -R airflow:root /opt/airflow && \
    chmod -R 777 /opt/airflow/logs

USER airflow