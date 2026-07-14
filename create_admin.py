from database import SessionLocal, engine
import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Check if admin already exists
admin = db.query(models.Admin).filter(models.Admin.email == "admin@portal.com").first()
if not admin:
    hashed_password = pwd_context.hash("admin123")
    new_admin = models.Admin(
        username="SuperAdmin",
        email="admin@portal.com",
        password_hash=hashed_password
    )
    db.add(new_admin)
    db.commit()
    print("Admin created successfully! Email: admin@portal.com, Password: admin123")
else:
    print("Admin already exists. Email: admin@portal.com, Password: admin123")

db.close()
