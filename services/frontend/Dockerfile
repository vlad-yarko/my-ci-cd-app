###
FROM node:20.14-bullseye-slim AS build

LABEL maintainer="vlad-yarko"
LABEL org.opencontainers.image.source="https://github.com/vlad-yarko/my-kubernetes"

WORKDIR /app

COPY package*.json ./

RUN --mount=type=cache,target=/app/.npm \
  npm set cache /app/.npm && \
  npm install

COPY . .

RUN npm run build


###
FROM nginxinc/nginx-unprivileged:1.23-alpine-perl AS prod


COPY --link nginx.conf /etc/nginx/conf.d/default.conf

COPY --link --from=build /app/dist/ /usr/share/nginx/html

EXPOSE 8080
