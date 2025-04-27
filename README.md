
# 🌪️ Hello FastAPI — Example FastAPI + GraphQl + Docker App + gRPC + Kafka + RabbitMQ

<p align="center">
  <img src="https://img.shields.io/badge/Build-Passing-brightgreen.svg" alt="Build Status">
  <img src="https://img.shields.io/badge/Docker-Ready-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/FastAPI-0.111.0-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.13.2-blue.svg" alt="Python Version">
</p>

---

This project is a minimal FastAPI app, Dockerized and ready to be used as a base for your next project, or as a guide to Dockerize your existing FastAPI app.

It wires up a lot of real-world components without overloading the project with too many personal preferences.

---

**⚡ Stack:**

- **FastAPI** 0.111.0
- **Python** 3.13.2

---

## 📚 Table of Contents

- [Tech Stack](#tech-stack)
- [Running the App](#running-the-app)
  - [Clone the Repo](#clone-the-repo)
  - [Build and Start](#build-and-start)
  - [Set Up the Database](#set-up-the-database)
  - [Visit in Browser](#visit-in-browser)
- [Optional Services](#optional-services)
  - [gRPC Support](#grpc-support)
  - [Kafka Support](#kafka-support)
  - [RabbitMQ Support](#rabbitmq-support)
- [Development Commands](#development-commands)
  - [Linting](#linting)
  - [Formatting](#formatting)
  - [Testing](#testing)
- [Managing Dependencies](#managing-dependencies)
- [Front-end Choices](#front-end-choices)
- [Notable Opinions and Extensions](#notable-opinions-and-extensions)
- [Additional Resources](#additional-resources)
- [About the Author](#about-the-author)

---

# ⚙️ Tech Stack

### Back-end

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [Redis](https://redis.io/)
- [Celery](https://github.com/celery/celery)
- Optional: [RabbitMQ](https://www.rabbitmq.com/), [Kafka](https://kafka.apache.org/), gRPC Reflection

### Front-end

- [esbuild](https://esbuild.github.io/)
- [TailwindCSS](https://tailwindcss.com/)
- [Heroicons](https://heroicons.com/)

---

# 🚀 Running the App

## 1. Clone the Repo

```bash
git clone https://github.com/your-username/your-repo.git hellofastapi
cd hellofastapi
```

## 2. Build and Start

```bash
docker compose up --build
```

**Note:**
- First build will take 5–10 minutes.
- Ensure Docker Compose v2.20.2+.
- Change `DOCKER_WEB_PORT_FORWARD` in `.env` if port 8000 is in use.
- Adjust `UID` and `GID` if permission errors on Linux.

## 3. Set Up the Database

```bash
./run fastapi db reset --with-testdb
```

## 4. Visit in Browser

```bash
http://localhost:8000
```

---

# 🚫 Optional Services

You can optionally enable gRPC, Kafka, and RabbitMQ by configuring your `.env` file.

## gRPC Support

Enable gRPC by setting:

```bash
ENABLE_GRPC=true
GRPC_PORT=50051
ENABLE_GRPC_REFLECTION=${DEBUG}
```

Ports for gRPC are exposed automatically if enabled.

Start gRPC services:

```bash
docker compose --profile web up
```

## Kafka Support

Enable Kafka by setting:

```bash
ENABLE_KAFKA=true
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

Kafka services like Zookeeper and Kafka will automatically run and be health-checked.

Start Kafka services:

```bash
docker compose --profile kafka up
```

## RabbitMQ Support

Enable RabbitMQ by setting:

```bash
ENABLE_RABBITMQ=true
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=true
```

RabbitMQ will expose ports 5672 (AMQP) and 15672 (Management UI).

Start RabbitMQ services:

```bash
docker compose --profile rabbitmq up
```

---

# 🛠️ Development Commands

## Linting

```bash
./run lint
```

## Formatting

```bash
./run format
```

## Testing

```bash
./run test
```

## Combo Command

```bash
./run quality
```

---

# 📦 Managing Dependencies

- **List outdated:**

```bash
./run uv:outdated
./run yarn:outdated
```

- **Install new packages:**

##### Option 1
1. Edit `pyproject.toml` or `assets/package.json`.
2. Run:

```bash
./run deps:install
```

##### Option 2
1. CLI Add:

```bash
./run uv add mypackage --no-sync
./run yarn add mypackage --no-lockfile
```

2. Then install:

```bash
./run deps:install
```

---

# 🎨 Front-end Choices

Pick your JS framework depending on your needs:

- [Hotwire](https://hotwired.dev/)
- [HTMX](https://htmx.org/)
- [AlpineJS](https://github.com/alpinejs/alpine)
- [Vue.js](https://vuejs.org/)
- [React.js](https://reactjs.org/)
- [jQuery](https://jquery.com/)

---

# 🧐 Notable Opinions and Extensions

| Feature               | Details                                                     |
| --------------------- | ----------------------------------------------------------- |
| **App Server**        | [uvicorn](https://www.uvicorn.org/)                         |
| **ORM**               | [SQLAlchemy](https://www.sqlalchemy.org/)                   |
| **Migrations**        | [Alembic](https://alembic.sqlalchemy.org/en/latest/)        |
| **Linting**           | [ruff](https://github.com/astral-sh/ruff)                   |
| **Testing**           | [pytest](https://github.com/pytest-dev/pytest) + pytest-cov |
| **Routing**           | `/` page and `/up` health check routes                      |
| **Config Management** | `.env` + `config/settings.py`                               |
| **Docker**            | Full multi-stage builds                                     |
| **CI**                | GitHub Actions setup                                        |
| **Package Manager**   | [uv](https://github.com/astral-sh/uv)                       |
| **Assets**            | TailwindCSS, esbuild, Heroicons                             |

---

# 📚 Additional Resources

- [Docker Official Docs](https://docs.docker.com/)
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Deploy FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Docker Compose Production Guide](https://docs.docker.com/compose/production/)

---

# 👨‍💻 About the Author

Thanks for checking out this project! Feel free to fork, clone, and improve.
