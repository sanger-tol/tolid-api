## Running with Docker

To run the app on a Docker container, please execute the following from the root directory:

```bash
# running the app (devlopment) - N.B. database will need initialising
docker-compose --env-file .env.dev up --build --abort-on-container-exit tolid-api tolid-ui tolid-db

# Running API tests
docker-compose --env-file .env.dev up --build --abort-on-container-exit tolid-api-test

# Running UI tests (watch mode)
docker-compose --env-file .env.dev up --build --abort-on-container-exit tolid-ui-test

```
Everything for staging and prod is built/tested/deployed via GitLab. Commit to the staging or production branch to trigger the pipeline.
