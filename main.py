from database import engine
from models import Base 

def create_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_db()
    print("✅ Database tables created successfully.")