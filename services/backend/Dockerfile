ARG PYTHON_VERSION=3.11-slim


###
FROM python:${PYTHON_VERSION} AS base

LABEL maintainer="vlad-yarko"
LABEL org.opencontainers.image.source="https://github.com/vlad-yarko/my-kubernetes"
# LABEL org.opencontainers.image.description=Logging/Monitoring

RUN useradd -m backend

WORKDIR /app

COPY --chown=backend requirements.txt .


###
FROM base AS prod

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=backend . .

EXPOSE 8000

# USER backend

ENTRYPOINT [ "uvicorn", "main:app" ]
CMD [ "--host", "0.0.0.0", "--port", "8000" ]
