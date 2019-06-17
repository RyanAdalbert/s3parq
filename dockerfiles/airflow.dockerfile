FROM puckel/docker-airflow:1.10.3

USER root

RUN apt-get update
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common \
    vim \
    git \
    inetutils-ping

ARG core_location=/usr/src/app/
RUN mkdir /usr/src/app
COPY ./requirements.txt $core_location/requirements.txt
WORKDIR $core_location
RUN pip install -r requirements.txt

ENV PYTHONPATH=/usr/local/lib/python3.6/site-packages:$core_location
COPY dockerfiles/entrypoints/airflow.sh /airflow-entrypoint.sh
COPY dockerfiles/configs/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
RUN chown -R airflow: ${AIRFLOW_HOME}

COPY . $core_location
COPY ./core/airflow/dags /root/airflow/dags

RUN python setup.py install

ENV AWS_DEFAULT_REGION="us-east-1"

WORKDIR ${AIRFLOW_HOME}
CMD ["/airflow-entrypoint.sh", "webserver"] # set default arg for entrypoint
