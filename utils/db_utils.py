from flask_sqlalchemy import SQLAlchemy

def get_db(db=None):
    if not db:
        db = SQLAlchemy()

    return db
    