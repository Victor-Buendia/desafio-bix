#!/bin/bash

OSTYPE=$(uname)

if ! [ -e .env ]; then
	echo """
BIX_DB_HOST=
BIX_DB_PORT=5432
BIX_DB_USER=
BIX_DB_PASS=
BIX_DB_NAME=postgres

BIX_ENDPOINT_FUNCIONARIOS=
BIX_ENDPOINT_CATEGORIAS=

DOCKER_DB_HOST=banco
DOCKER_DB_PORT=5432
	""" > .env
fi

if [ $OSTYPE = "Linux" ]; then ISLINUX="True"; else ISLINUX="False"; fi

if ! $(grep -Fq "AIRFLOW_UID" .env) && $ISLINUX; then
	echo "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" >> .env
fi