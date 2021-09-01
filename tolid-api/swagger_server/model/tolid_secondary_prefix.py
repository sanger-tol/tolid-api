from .base import Base, db


class TolidSecondaryPrefix(Base):
    __tablename__ = "secondary_prefix"
    letter = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    primary_prefix_letter = db.Column(db.String(), db.ForeignKey('primary_prefix.letter'),
                                      primary_key=True)
    primary_prefix = db.relationship("TolidPrimaryPrefix", back_populates="secondary_prefixes",
                                     foreign_keys=[primary_prefix_letter])

    def to_dict(cls):
        return {'letter': cls.letter,
                'name': cls.name}
