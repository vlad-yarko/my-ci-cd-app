###
FROM node:20-bullseye-slim AS build
# FROM node:20.14-bullseye-slim AS build

LABEL maintainer="vlad-yarko"
LABEL org.opencontainers.image.source="https://github.com/vlad-yarko/my-kubernetes"

WORKDIR /app

RUN apt-get update && apt-get install -y python3 make g++

COPY package.json yarn.lock ./

# RUN yarn install --immutable
RUN yarn install

COPY . .

RUN yarn build


###
FROM nginxinc/nginx-unprivileged:1.23-alpine-perl AS prod


COPY --link nginx.conf /etc/nginx/conf.d/default.conf

COPY --link --from=build /app/dist/ /usr/share/nginx/html

EXPOSE 8080
