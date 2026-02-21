from fastapi import FastAPI

# API Routes
from api.routes.polls import router as polls_router
from api.routes.questions import router as questions_router
from api.routes.options import router as options_router
from api.routes.votes import router as votes_router

from db.init_db import init_db

app = FastAPI(title="Poll Service", description="Poll Service API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()  # ✅ OK for now (dev / pre-Alembic)

@app.get('/')
def home():
    return {'message': 'Welcome to the Poll System'}

@app.get('/health')
def health():
    return {'message': 'OK'}

# Routes
app.include_router(polls_router, prefix='/polls')

# Internal Routes
app.include_router(questions_router, prefix='/internal/questions')
app.include_router(options_router, prefix='/internal/options')
app.include_router(votes_router, prefix='/internal/votes')