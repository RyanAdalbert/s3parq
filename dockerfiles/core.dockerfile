FROM python:3.6-slim

# Airflow
ARG AIRFLOW_VERSION=1.10.2
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_GPL_UNIDECODE yes

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install --upgrade pip \
    && pip install pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install jupyter \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && pip install 'redis>=2.10.5,<3' \
    # && if [ -n "${PYTHON_DEPS_FILE}" ]; then pip install -r ${PYTHON_DEPS_FILE}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

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

#Install docker
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
# Do we want to specify a specific release?
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
RUN apt-get update
RUN apt-get install -y docker-ce

ARG core_location=/usr/src/app/
RUN mkdir /usr/src/app
COPY ./requirements.txt $core_location/requirements.txt
WORKDIR $core_location
RUN pip install -r requirements.txt

ENV PYTHONPATH=/usr/local/lib/python3.6/site-packages:$core_location
COPY dockerfiles/entrypoints/airflow.sh /airflow-entrypoint.sh
COPY dockerfiles/configs/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY dockerfiles/configs/jupyter.py /notebook/jupyter_notebook_config.py
COPY dockerfiles/entrypoints/notebook.sh /notebook-entrypoint.sh
RUN chown -R airflow: ${AIRFLOW_HOME}

COPY . $core_location
COPY ./core/airflow/dags /root/airflow/dags

# remove the enum package that some jerkface dependency is installing
RUN rm -r /usr/local/lib/python3.6/site-packages/enum \
    && rm -r /usr/local/lib/python3.6/site-packages/enum34-1.1.6.dist-info

RUN python setup.py install

EXPOSE 8080 5555 8793

ENV AWS_DEFAULT_REGION="us-east-1"

WORKDIR ${AIRFLOW_HOME}
# ENTRYPOINT ["/entrypoint.sh"]
CMD ["/airflow-entrypoint.sh", "webserver"] # set default arg for entrypoint
