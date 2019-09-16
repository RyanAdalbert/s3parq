#!/usr/bin/env bash

# Check that AIRFLOW_HOME is defined correctly in the environment before continuing
if [ $AIRFLOW_HOME != "/usr/local/airflow" ]; then
    echo "AIRFLOW_HOME is not set to /usr/local/airflow"
    echo "Killing entrypoint script..."
    sleep 10
    exit 1
fi
# echo "AIRFLOW HOME VALUE IS:"
# echo $AIRFLOW_HOME

TRY_LOOP="20"

: "${REDIS_HOST:="redis"}"
: "${REDIS_PORT:="6379"}"
: "${REDIS_PASSWORD:=""}"

# Dummy environment vars required for Airflow to run
: "${MYSQL_HOST:="dummy-host"}"
: "${MYSQL_PORT:="dummy-port"}"
: "${MYSQL_USER:="dummy-user"}"
: "${MYSQL_PASSWORD:="dummy-password"}"
: "${MYSQL_DB:="dummy-db"}"

# Local (default) configurations. Overridden by AWS environment variables in the cloud
: "${POSTGRES_HOST:="airflowpg"}"
: "${POSTGRES_PORT:="5432"}"
: "${POSTGRES_USER:="airflow"}"
: "${POSTGRES_PASSWORD:="airflow"}"
: "${POSTGRES_DB:="airflow"}"

# Defaults and back-compat
: "${AIRFLOW__CORE__FERNET_KEY:=${FERNET_KEY:=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")}}"
: "${AIRFLOW__CORE__EXECUTOR:=${EXECUTOR:-Local}Executor}"

export \
  AIRFLOW__CELERY__BROKER_URL \
  AIRFLOW__CELERY__RESULT_BACKEND \
  AIRFLOW__CORE__EXECUTOR \
  AIRFLOW__CORE__FERNET_KEY \
  AIRFLOW__CORE__LOAD_EXAMPLES \
  AIRFLOW__CORE__SQL_ALCHEMY_CONN \


# Load DAGs exemples (default: Yes)
AIRFLOW__CORE__LOAD_EXAMPLES=False

# This now gets taken care of in the dockerfile
# Install custom python package if requirements.txt is present
# if [ -e "/requirements.txt" ]; then
#     $(which pip) install --user -r /requirements.txt
# fi

if [ -n "$REDIS_PASSWORD" ]; then
    REDIS_PREFIX=:${REDIS_PASSWORD}@
else
    REDIS_PREFIX=
fi

# Makes sure airflow can connect to its metadatabase
wait_for_port() {
  local name="$1" host="$2" port="$3"
  local j=0
  while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
    j=$((j+1))
    if [ $j -ge $TRY_LOOP ]; then
      echo >&2 "$(date) - $host:$port still not reachable, giving up"
      exit 1
    fi
    echo "$(date) - waiting for $name... $j/$TRY_LOOP"
    sleep 5
  done
}

export AIRFLOW__CORE__BASE_LOG_FOLDER=/usr/local/airflow/logs

echo "$AIRFLOW__CORE__EXECUTOR"

if [ "$AIRFLOW__CORE__EXECUTOR" != "SequentialExecutor" ]; then
  AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"
  AIRFLOW__CELERY__RESULT_BACKEND="db+postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"
  wait_for_port "$DB_TYPE" "$POSTGRES_HOST" "$POSTGRES_PORT"
  echo "Connected to $AIRFLOW__CORE__SQL_ALCHEMY_CONN."
fi

if [ "$AIRFLOW__CORE__EXECUTOR" = "CeleryExecutor" ]; then
  AIRFLOW__CELERY__BROKER_URL="redis://$REDIS_PREFIX$REDIS_HOST:$REDIS_PORT/1"
  wait_for_port "Redis" "$REDIS_HOST" "$REDIS_PORT"
fi

case "$1" in
  webserver)
    if [ "${INITDB:=n}" == "y" ]; then
      echo "Initializing Airflow db..."
      airflow initdb
    fi

    if [ "$AIRFLOW__CORE__EXECUTOR" = "LocalExecutor" ]; then
      # With the "Local" executor it should all run in one container.
      echo "Launching Airflow scheduler..."
      airflow scheduler &
    fi
    echo "Launching Airflow webserver..."
    exec airflow webserver -p 8008
    ;;
  worker|scheduler)
    # To give the webserver time to run initdb.
    sleep 10
    exec airflow "$@"
    ;;
  flower)
    exec airflow "$@"
    ;;
  version)
    exec airflow "$@"
    ;;
  *)
    # The command is something like bash, not an airflow subcommand. Just run it in the right environment.
    exec "$@"
    ;;
esac
