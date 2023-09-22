from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mangamonster.settings as config

def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            config.DBUSERNAME, config.DBPASSWORD, config.DBHOST, config.DBPORT, config.DBNAME
        )
)
    
def db_connect():
    engine = get_connection()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db