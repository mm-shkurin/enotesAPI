from database.db import Base,engine
from models import *

if __name__=="main":
    print("Creating database ....")
    Base.metadata.create_all(engine)
