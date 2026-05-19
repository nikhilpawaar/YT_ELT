##FROM ubuntu:latest
##LABEL authors="Nikhil"
##
##ENTRYPOINT ["top", "-b"]
#
#ARG AIRFLOW_VERSION=2.9.2
#ARG PYTHON_VERSION=3.10
#
#FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}
#
#ENV AIRFLOW_HOME=/opt/airflow
#
#COPY requirements.txt /
#
#RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt


ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

ENV AIRFLOW_HOME=/opt/airflow

USER root

COPY requirements.txt /

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -r /requirements.txt

# Create required folders and fix permissions
RUN mkdir -p /opt/airflow/logs/scheduler && \
    chown -R airflow:root /opt/airflow && \
    chmod -R 775 /opt/airflow

# VERY IMPORTANT
USER airflow