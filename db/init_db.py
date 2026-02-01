from db.session import engine
from db.base import Base

# IMPORTANT: import all models so they register with Base
from models.poll import Poll
from models.question import Question
from models.option import Option
from models.vote import Vote

def init_db():
    Base.metadata.create_all(bind=engine)
