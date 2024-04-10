# OSINT Meta Scanner

## Pre-requisites

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [Node.js](https://nodejs.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [`just`](https://github.com/casey/just)
  > [!NOTE]
  > We use `just` as a task runner. It automatically loads the `.env` file and sets the environment variables.
- [direnv](https://direnv.net/) (optional)

## Development

1. Install dependencies
   ```sh
   poetry install
   ```
2. Start the PostgreSQL database and Redis server
   ```sh
   docker compose -f compose.dev.yaml up -d
   ```
3. Copy the `.env.example` file to `.env` and fill in the required values
4. Run the migrations
   ```sh
   just alembic upgrade head
   ```
5. Run the application server
   ```sh
   just server
   ```
6. Run the Celery worker
   ```sh
   just celery worker --loglevel=INFO
   ```
7. Change directory into the client app and run its development server:
   ```sh
   cd client/
   npm run dev
   ```

## Deployment

Use the included `compose.yaml` file as an example deployment configuration.

1. Start the services
   ```sh
   docker compose up -d
   ```
2. Run the migrations
   ```sh
    docker compose exec app alembic upgrade head
   ```
3. Access the application at http://localhost:8080
