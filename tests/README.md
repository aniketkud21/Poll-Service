# 🧪 Testing Guide

This directory contains automated tests for the Poll Service. We use `pytest` as our primary testing framework.

## 🚀 How to Run Tests

Ensure you have the environment set up and dependencies installed with `uv sync`.

### Run All Tests

```bash
uv run pytest
```

### Run Specific Test File

```bash
uv run pytest tests/test_poll_service.py
```

### Run with Verbose Output

```bash
uv run pytest -v
```

---

## 🛠️ Infrastructure

The testing setup consists of:

- **`pyproject.toml`**: Configured with `pythonpath = ["."]` to allow importing from the root directory.
- **`tests/conftest.py`**: Contains shared fixtures, most notably `db_session`.
- **`db/session.py`**: Configured with `expire_on_commit=False` to ensure objects remain accessible after a database commit.

---

## ➕ How to Add Tests

### 1. Naming Convention

- Test files should be named `test_*.py`.
- Test functions should start with `test_`.

### 2. Using Fixtures

The most important fixture is `db_session`, which provides a clean SQLAlchemy session for each test.

```python
def test_my_new_feature(db_session):
    # Your test logic here
    pass
```

### 3. Example Test Pattern

When testing services, we usually follow the AAA (Arrange, Act, Assert) pattern:

```python
from api.schemas.poll import PollCreate
from services.poll_service import PollService

def test_example(db_session):
    # 1. Arrange: Create a payload
    payload = PollCreate(
        title="Test",
        poll_type="POLL",
        questions=[...]
    )

    # 2. Act: Call the service
    result = PollService.create_poll(payload)

    # 3. Assert: Verify results
    assert result.poll_id is not None
```

---

## 🏗️ Database Setup for Tests

The `setup_db` fixture in `conftest.py` automatically runs `Base.metadata.create_all(bind=engine)` to ensure the schema exists.

> [!TIP]
> Tests currently run against the database specified in your `.env`. For a dedicated test database, consider using a separate `.env.test` file or overriding `DATABASE_URL` in your shell.
