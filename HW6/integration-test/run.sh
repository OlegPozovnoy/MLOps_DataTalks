#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

pytest ../tests/test_batch.py

docker compose up -d

sleep 5

aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration || true
aws --endpoint-url=http://localhost:4566 s3 ls

cd ../
pipenv run python ./integration-test/integration_test.py
cd ./integration-test/


aws --endpoint-url=http://localhost:4566 s3 ls s3://nyc-duration/in/


ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker compose down

ERROR_CODE=$?
echo ${ERROR_CODE}