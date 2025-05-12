FROM public.ecr.aws/ubuntu/ubuntu:25.10 AS base
COPY --from=ghcr.io/astral-sh/uv:0.7.3 /uv /uvx /bin/

WORKDIR /app
ENV PYTHONPATH=/app

COPY . .
RUN uv sync --frozen
