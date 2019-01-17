FROM python:3.7

WORKDIR /usr/src/app

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py install
ENTRYPOINT ["corecli"]
CMD []