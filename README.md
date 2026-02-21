# 🗳️ Poll Service API

A robust, asynchronous Poll Management Service built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. This project provides a full suite of RESTful endpoints to create, manage, and participate in polls.

## 🚀 Features

- **Poll Management**: Create, view, update, and delete polls with customizable titles, descriptions, and expiry dates.
- **Question & Options**: Structured relationship between polls, questions, and voting options.
- **Voting System**: Secure voting mechanism with UUID-based tracking.
- **Auto Database Initialization**: Automatically sets up your PostgreSQL schema on startup.
- **Modern Python Tooling**: Uses `uv` for lightning-fast dependency management and environment isolation.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Environment Management**: [python-dotenv](https://github.com/theskumar/python-dotenv)

## 📋 Prerequisites

- Python 3.12+ (or 3.14 for native `uuid7` support)
- PostgreSQL database
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## ⚙️ Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd poll-service
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the root directory:

   ```env
   DATABASE_URL="postgresql://username:password@localhost:5432/poll_service"
   ```

3. **Install Dependencies**:
   ```bash
   uv sync
   ```

## 🏃 Running the Application

Start the development server with hot-reload enabled:

```bash
uv run uvicorn api.server:app --reload --port 8081
```

The API will be available at `http://127.0.0.1:8081`.

## 📖 API Documentation

Once the server is running, you can access the interactive documentation:

- **Swagger UI**: [http://127.0.0.1:8081/docs](http://127.0.0.1:8081/docs)
- **ReDoc**: [http://127.0.0.1:8081/redoc](http://127.0.0.1:8081/redoc)

### Key Endpoints

| Method | Endpoint              | Description                              |
| ------ | --------------------- | ---------------------------------------- |
| `POST` | `/polls`              | Create a new poll (nested structure)     |
| `GET`  | `/polls`              | List all polls                           |
| `GET`  | `/polls/{id}`         | Get detailed poll with questions/options |
| `POST` | `/internal/questions` | Create question (standalone)             |
| `POST` | `/internal/options`   | Create option (standalone)               |
| `POST` | `/internal/votes`     | Cast a vote                              |

## 🏗️ Project Structure

```text
poll-service/
├── api/
│   ├── routes/      # FastAPI route definitions
│   ├── schemas/     # Pydantic validation models
│   └── server.py    # Application entry point
├── db/              # Database connection and session management
├── models/          # SQLAlchemy database models
├── repositories/    # Data access layer
├── services/        # Business logic layer
├── tests/           # Automated test suite
├── pyproject.toml   # Project dependencies and metadata
└── .env             # Environment configuration (secrets)
```

## 🧪 Testing

The project uses `pytest` for automated testing.

### Running Tests

To run all tests, use the following command:

```bash
uv run pytest
```

For more detailed information on testing, refer to the [Tests README](tests/README.md).

## 📝 License

This project is licensed under the MIT License.
