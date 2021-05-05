## Running with Docker

To run the app on a Docker container, first you will need to set up a file with the necessary environment variables. Let's call this .env.dev (there is a template file .env.template you can use as a template!). Then, execute the following from the root directory:

```bash
# running the app (devlopment) - N.B. database will need initialising
docker-compose --env-file .env.dev up --build --abort-on-container-exit tolid-api tolid-ui tolid-db

# Running API tests
docker-compose --env-file .env.dev up --build --abort-on-container-exit tolid-api-test

# Running UI tests (watch mode)
docker-compose --env-file .env.dev up --build --abort-on-container-exit tolid-ui-test

```
Everything for staging and prod is built/tested/deployed via GitLab. Commit to the staging or production branch to trigger the pipeline.
