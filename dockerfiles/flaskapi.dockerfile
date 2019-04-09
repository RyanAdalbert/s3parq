FROM python:3.6-slim



# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install --upgrade pip \
    ## pin version?
    && pip install flask 

COPY ./core/api/ /app/
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["/app/app.py"]
