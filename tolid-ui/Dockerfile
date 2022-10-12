# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

# This is used for a production build
# stage 1 as builder
FROM node:12-alpine as builder

RUN apk add yarn
RUN mkdir /workspace

WORKDIR /workspace

RUN echo \"@tol:registry\" \"https://gitlab.internal.sanger.ac.uk/api/v4/projects/3596/packages/npm/\" >> .yarnrc

COPY app/ .
RUN yarn install --ignore-engines
RUN yarn build

# Stage 2
FROM nginx:alpine

COPY nginx/* /etc/nginx/

## Remove default nginx index page
RUN rm -rf /var/www/tolid-ui/*

# Copy from the stage 1
COPY --from=builder /workspace/build/ /var/www/tolid-ui/

EXPOSE 80
