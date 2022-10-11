# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

# This is used for a production build
# stage 1 as builder
FROM node:12-alpine as builder

RUN npm install react-scripts@2.1.8 -g --silent
RUN mkdir /workspace

WORKDIR /workspace

RUN echo \"@tol:registry\" \"https://gitlab.internal.sanger.ac.uk/api/v4/projects/3596/packages/npm/\" >> .yarnrc

COPY ./app/package.json ./

RUN yarn install

COPY app/ .

# Stage 2
FROM nginx:alpine

COPY nginx/* /etc/nginx/

## Remove default nginx index page
RUN rm -rf /var/www/tolid-ui/*

# Copy from the stage 1
COPY --from=builder /workspace/build/ /var/www/tolid-ui/

EXPOSE 80
