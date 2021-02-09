## Running with Docker

To run the app on a Docker container, please execute the following from the root directory:

```bash
# running the app (devlopment) - N.B. database will need initialising
docker-compose --env-file .env.dev up --build --abort-on-container-exit api ui db
# setting up test environment and running tests
docker-compose --env-file .env.dev up --build --abort-on-container-exit api-tests

# UAT
docker-compose --env-file .env.uat up --build --abort-on-container-exit api ui

# Prod
docker-compose --env-file .env.prod up --build --abort-on-container-exit api ui

```