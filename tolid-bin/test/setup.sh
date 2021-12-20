#!/bin/sh
# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

# set the env file to default to .env.dev if no argument specified
TEST_ENV_FILE="${1:-.env.dev}"

# start everything
docker-compose --env-file "$TEST_ENV_FILE" up -d --build tolid-api tolid-ui tolid-db tolid-selenium-chrome
