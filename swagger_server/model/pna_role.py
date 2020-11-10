from .base import Base, db

class PnaRole(Base):
    __tablename__ = "role"
    role_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("PnaUser", uselist=False, foreign_keys=[user_id])
