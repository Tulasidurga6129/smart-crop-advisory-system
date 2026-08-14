from app.core.database import Base, engine
from app.models.user import User


def init_db():
    Base.metadata.create_all(bind=engine)
    print("DATABASE TABLES CREATED SUCCESSFULLY")


if __name__ == "__main__":
    init_db()