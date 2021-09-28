from .base import Base, db


class TolidUser(Base):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    organisation = db.Column(db.String(), nullable=True)
    api_key = db.Column(db.String(), nullable=True, unique=True)
    token = db.Column(db.String(), nullable=True, unique=True)
    roles = db.relationship('TolidRole', lazy=False, back_populates="user")

    def to_dict(cls):
        return {'name': cls.name,
                'email': cls.email,
                'organisation': ("" if cls.organisation is None else cls.organisation),
                'roles': cls.roles}
