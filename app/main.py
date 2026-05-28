from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.database import Base, engine
from app.routers import auth, todos

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _create_default_user()
    yield


def _create_default_user():
    from app.auth import get_password_hash
    from app.database import SessionLocal
    from app.models import User

    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "Haydee").first():
            db.add(User(username="Haydee", hashed_password=get_password_hash("Summer")))
            db.commit()
    finally:
        db.close()


app = FastAPI(
    title="TODO List API",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/")
def serve_frontend():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/login")
def serve_login():
    return FileResponse(str(FRONTEND_DIR / "login.html"))
