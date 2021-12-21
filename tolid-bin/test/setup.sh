#!/bin/sh
# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

# set the env file to default to .env.dev if no argument specified
TEST_ENV_FILE="${1:-.env.dev}"

# start everything
docker-compose \
    --env-file "$TEST_ENV_FILE" \
    -f tolid-automated-test/docker-compose.automation.yml \
    up -d \
    --build \
    tolid-api tolid-ui tolid-db tolid-selenium-chrome tolid-api-test tolid-report-server && \

# wait 60 seconds (after announcing)
echo && \
echo 'Waiting for the database to create' && \
sleep 60s && \

# print the link
echo && \
echo 'Everything is setup! Go to http://localhost:7902'
