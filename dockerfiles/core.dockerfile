FROM python:3.7

WORKDIR /usr/src/app

# install docker client
RUN apt-get update
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
# Do we want to specify a specific release?
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
RUN apt-get update
RUN apt-get install -y docker-ce 

# install python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy all of the source across
COPY . ./
RUN python setup.py install
ENTRYPOINT ["corecli"]
CMD []