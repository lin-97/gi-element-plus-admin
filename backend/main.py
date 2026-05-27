from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, menu, role, student, user
from app.core.database import Base, SessionLocal, engine
from app.db.gender_migration import migrate_student_gender
from app.db.system_rbac_migration import migrate_system_rbac


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        migrate_student_gender(db)
        migrate_system_rbac(db)
    finally:
        db.close()
    yield


app = FastAPI(title="学生信息管理系统", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(student.router, prefix="/api")
app.include_router(menu.router, prefix="/api")
app.include_router(role.router, prefix="/api")
app.include_router(user.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "gi-admin API"}


@app.get("/health")
def health():
    return {"status": "ok"}
