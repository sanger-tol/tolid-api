# SPDX-FileCopyrightText: 2023 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from tol.api_base.model import Base, db, setup_model


@setup_model
class Species(Base):
    __tablename__ = 'species'

    class Meta:
        type_ = 'species'
        id_column = 'taxonomy_id'

    taxonomy_id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String())
    name = db.Column(db.String())
    common_name = db.Column(db.String())
    genus = db.Column(db.String())
    family = db.Column(db.String())
    tax_order = db.Column(db.String())
    tax_class = db.Column(db.String())
    phylum = db.Column(db.String())
    kingdom = db.Column(db.String())
    specimen = db.relationship('Specimen', back_populates='species',
                               lazy=False, order_by='Specimen.number')
