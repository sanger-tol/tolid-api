from .base import Base, db


class TolidUser(Base):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    organisation = db.Column(db.String(), nullable=False)
    api_key = db.Column(db.String(), nullable=False, unique=True)

    def to_dict(cls):
        return {'name': cls.name,
                'email': cls.email,
                'organisation': cls.organisation}
