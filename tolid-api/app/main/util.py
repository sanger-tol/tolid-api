# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from datetime import datetime

def current_highest_tolid_number(species):
    # What is the current highest specimen number?
    # This is inefficient but we don't currently have ability to sort
    highest = 0
    for specimen in species.specimens:
        if specimen.number > highest:
            highest = specimen.number
    return highest

def create_new_tolid(session, species, specimen_id, requested_taxonomy_id, user):
    # What is the current highest specimen number?
    number = current_highest_tolid_number(species)
    tolid = session.data_object_factory(
        'specimen',
        f'{species.prefix}{number + 1}',
        attributes={
            'specimen_id': specimen_id,
            'number': number + 1,
            'requested_taxonomy_id': requested_taxonomy_id,
            'created_at': datetime.now(),
        },
        to_one={
            'species': species,
            'user': user
        }
    )
    return tolid
