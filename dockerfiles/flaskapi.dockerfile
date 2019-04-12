FROM python:3.6-slim


ENV PYTHONPATH=/usr/local/lib/python3.6/site-packages:/core

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

COPY ./ /core/    
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential git
RUN pip install --upgrade pip \
    && pip install -r /core/requirements/api.txt
WORKDIR /core
EXPOSE 5000
#ENTRYPOINT ["python3"]
#CMD ["./core/api/app.py"]
CMD tail -f /dev/null
