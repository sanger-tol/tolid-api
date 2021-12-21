#!/bin/sh
# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

# set the env file to default to .env.dev if no argument specified
TEST_ENV_FILE="${1:-.env.dev}"

# build the runner
docker-compose \
    --env-file "$TEST_ENV_FILE" \
    -f tolid-automated-test/docker-compose.automation.yml \
    build tolid-automated-test

# run the test
docker-compose \
    --env-file "$TEST_ENV_FILE" \
    -f tolid-automated-test/docker-compose.automation.yml \
    run tolid-automated-test robot -d /tests test.robot
