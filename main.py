from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import init_db, SessionLocal
from models.user import User, UserRole, UserStatus
from core.security import get_password_hash
from core.config import settings

from api import auth, admin, institute, regulatory, activities, news, contact

app = FastAPI(
    title="TMSITI API",
    version="1.0.0",
    description="Toshkent shahar me'morchilik va shaharsozlik ilmiy-tadqiqot instituti rasmiy API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(institute.router, prefix="/api/v1")
app.include_router(regulatory.router, prefix="/api/v1")
app.include_router(activities.router, prefix="/api/v1")
app.include_router(news.router, prefix="/api/v1")
app.include_router(contact.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "TMSITI API ishga tushdi."}

@app.on_event("startup")
def on_startup():
    init_db()

    db = SessionLocal()
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD

    existing_admin = db.query(User).filter(User.email == admin_email).first()

    if not existing_admin:
        admin_user = User(
            email=admin_email,
            full_name="Super Admin",
            phone_number="+998770000194",
            password_hash=get_password_hash(admin_password),
            role=UserRole.superadmin,
            status=UserStatus.active,
            is_active=True,
            email_verified=True
        )
        db.add(admin_user)
        db.commit()
        print(f"\u2705 Superadmin yaratildi: {admin_email}")
    else:
        print(f"\u2139\ufe0f Admin allaqachon mavjud: {admin_email}")

    db.close()
