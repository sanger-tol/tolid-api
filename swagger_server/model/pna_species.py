from .base import Base, db

class PnaSpecies(Base):
    __tablename__ = "species"
    taxonomy_id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String())
    name = db.Column(db.String())
    common_name = db.Column(db.String())
    genus = db.Column(db.String())
    family = db.Column(db.String())
    tax_order = db.Column(db.String())
    tax_class = db.Column(db.String())
    phylum = db.Column(db.String())
    specimens = db.relationship('PnaSpecimen', lazy=False)

    def __str__(self):
        return "PnaSpecies: "+str(self.taxonomy_id)+", "+self.name