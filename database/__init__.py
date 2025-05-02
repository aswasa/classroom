from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import event


SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI)
localSession = sessionmaker(bind = engine)
Base = declarative_base()

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

Base.metadata.create_all(engine)

def get_db():
    db = localSession()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()