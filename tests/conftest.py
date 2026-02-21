import pytest
from db.session import Session, engine
from db.base import Base
# Import all models to ensure they are registered with Base
from models.poll import Poll
from models.question import Question
from models.option import Option
from models.vote import Vote

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # We could drop tables here if we want a clean slate for each run
    # Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
