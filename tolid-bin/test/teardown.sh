#!/bin/sh
# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

# set the env file to default to .env.dev if no argument specified
TEST_ENV_FILE="${1:-.env.dev}"

# stop everything and teardown
docker-compose --env-file "$TEST_ENV_FILE" -f tolid-automated-test/docker-compose.automation.yml down --remove-orphans
