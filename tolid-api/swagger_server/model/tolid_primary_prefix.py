from .base import Base, db


class TolidPrimaryPrefix(Base):
    __tablename__ = "primary_prefix"
    letter = db.Column(db.String, primary_key=True)
    name = db.Column(db.String())
    secondary_prefixes = db.relationship('TolidSecondaryPrefix', back_populates="primary_prefix",
                                         lazy=False, order_by='TolidPrimaryPrefix.letter')

    def to_dict(cls):
        return {'letter': cls.letter,
                'name': cls.name,
                'secondaryPrefixes': cls.secondary_prefixes}
