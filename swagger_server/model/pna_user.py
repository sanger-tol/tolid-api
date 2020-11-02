from .base import Base, db

class PnaUser(Base):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    api_key = db.Column(db.String(), nullable=False, unique=True)
