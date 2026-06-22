from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, SessionLocal
from .seed import seed
from .routers import auth, catalog, profile, matching, favorites

app = FastAPI(title="POSTSCHOOL API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(profile.router)
app.include_router(matching.router)
app.include_router(favorites.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
