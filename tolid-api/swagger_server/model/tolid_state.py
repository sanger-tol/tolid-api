from .base import Base, db


class TolidState(Base):
    __tablename__ = "state"
    state = db.Column(db.String(), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def to_dict(cls):
        return {'state': cls.state}
