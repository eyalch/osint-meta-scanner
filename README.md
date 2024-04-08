# OSINT Scanner

## Development

### Pre-requisites

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [`just`](https://github.com/casey/just)
  > [!NOTE]
  > We use `just` as a task runner. It automatically loads the `.env` file and sets the environment variables.
- [direnv](https://direnv.net/) (optional)

### Setup

1. Clone the repository
2. Install dependencies
    ```sh
    poetry install
    ```
3. Start the PostgreSQL database and Redis server
    ```sh
    docker compose up -d
    ```
4. Copy the `.env.example` file to `.env` and fill in the required values
5. Run the migrations
    ```sh
    just alembic upgrade head
    ```
6. Run the application server
    ```sh
    just server
    ```
7. Run the Celery worker
    ```sh
    just celery worker --loglevel=INFO
    ```
