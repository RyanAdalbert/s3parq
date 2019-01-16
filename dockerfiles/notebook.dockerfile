FROM jupyter/pyspark-notebook

USER root

ENV HADOOP_VERSION_MAJOR 2.7
ENV HADOOP_VERSION_FULL 2.7.6
ENV AWS_JAVA_SDK_VERSION 1.7.4
ENV MYSQL_CONNECTOR_VERSION 5.1.46

# MySQL jar
RUN wget -q https://repo1.maven.org/maven2/mysql/mysql-connector-java/${MYSQL_CONNECTOR_VERSION}/mysql-connector-java-${MYSQL_CONNECTOR_VERSION}.jar -P $SPARK_HOME/jars

# Hadoop for S3
RUN wget -q http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION_FULL}/hadoop-aws-${HADOOP_VERSION_FULL}.jar -P $SPARK_HOME/jars

# AWS SDK
RUN wget -q http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/${AWS_JAVA_SDK_VERSION}/aws-java-sdk-${AWS_JAVA_SDK_VERSION}.jar -P $SPARK_HOME/jars

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN fix-permissions $CONDA_DIR

USER $NB_UID

ENTRYPOINT ["/usr/local/bin/start-notebook.sh"]