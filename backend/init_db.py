# init_db.py
from poopers.backend.database import Base, engine
import poopers.backend.models as models  # make sure models are imported so Base knows about them

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
