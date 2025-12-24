from prometheus_client import (
    Counter,
    Gauge,
    Histogram
)


REQUESTS = Counter(
    "fastapi_requests_total",
    "Total number of HTTP requests",
    ["path", "app_name"]
)

RESPONSES = Counter(
    "fastapi_responses_total",
    "Total number of HTTP responses",
    ["path", "status_code", "app_name"]
)

EXCEPTIONS = Counter(
    "fastapi_exceptions_total",
    "Total number of HTTP exceptions",
    ["app_name", "path"]
)

REQUEST_LATENCY = Histogram(
    "fastapi_requests_duration_seconds",
    "Request duration in seconds",
    ["path", "app_name"]
)

IN_PROGRESS = Gauge(
    "fastapi_requests_in_progress",
    "Requests currently in progress",
    ["path", "app_name"]
)
