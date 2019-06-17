FROM jupyter/minimal-notebook

USER root

RUN pip install --upgrade pip \
    && pip install pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install 'redis>=2.10.5,<3'

ARG core_location=/usr/src/app
RUN mkdir /usr/src/app
COPY ./requirements.txt $core_location/requirements.txt
WORKDIR $core_location
RUN pip install -r requirements.txt

ENV PYTHONPATH=/usr/local/lib/python3.6/site-packages:$core_location
COPY dockerfiles/configs/jupyter.py /notebook/jupyter_notebook_config.py
COPY dockerfiles/entrypoints/notebook.sh /notebook-entrypoint.sh

ENV AWS_DEFAULT_REGION="us-east-1"

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
