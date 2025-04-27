# Build Python environment
FROM python:3.13.2-slim-bookworm AS app-build
LABEL maintainer="Moses <webdev2123@gmail.com>"

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
  && chown python:python -R /app

COPY --from=ghcr.io/astral-sh/uv:0.6.9 /uv /uvx /usr/local/bin/

USER python

COPY --chown=python:python pyproject.toml uv.lock* ./
COPY --chown=python:python bin/ ./bin

ENV PYTHONUNBUFFERED="true" \
  PYTHONPATH="." \
  UV_COMPILE_BYTECODE=1 \
  UV_PROJECT_ENVIRONMENT="/home/python/.local" \
  PATH="${PATH}:/home/python/.local/bin" \
  USER="python"

RUN chmod 0755 bin/* && bin/uv-install

# ← COPY the proto (or the whole hello/ dir) so protoc can see it
COPY --chown=python:python hello/central/user_service.proto hello/central/

# Install gRPC tools and compile our .proto into Python stubs
RUN python -m grpc_tools.protoc \
  -I. \
  --python_out=. \
  --grpc_python_out=. \
  hello/central/user_service.proto

CMD ["bash"]

###############################################################################
# Production app image
FROM python:3.13.2-slim-bookworm AS app
LABEL maintainer="Moses <webdev2123@gmail.com>"

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
  && chown python:python -R /app

USER python

ARG WEB_RELOAD="false"
ENV WEB_RELOAD="${WEB_RELOAD}" \
  PYTHONUNBUFFERED="true" \
  PYTHONPATH="." \
  UV_PROJECT_ENVIRONMENT="/home/python/.local" \
  PATH="${PATH}:/home/python/.local/bin" \
  USER="python"

COPY --chown=python:python --from=app-build /home/python/.local /home/python/.local
COPY --from=app-build /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/
COPY --chown=python:python . .

# 2) Copy the generated proto stubs
COPY --from=app-build /app/hello/central/user_service_pb2.py hello/central/
COPY --from=app-build /app/hello/central/user_service_pb2_grpc.py hello/central/

# 3) (Optional) if you have other files under hello/central you want too,
#    you can also do:
#    COPY --from=app-build /app/hello/central hello/central

# Uvicorn will serve FastAPI app
ENTRYPOINT ["/app/bin/docker-entrypoint-web"]

EXPOSE 8000


