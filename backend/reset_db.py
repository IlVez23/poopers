from sqlalchemy import text
from database import engine, Base
import models

def reset_database():
    # Drop all tables
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS questionnaire_responses CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS user_poops CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully!")

if __name__ == "__main__":
    reset_database() 