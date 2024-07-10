# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

def current_highest_tolid_number(species):
    # What is the current highest specimen number?
    # This is inefficient but we don't currently have ability to sort
    highest = 0
    for specimen in species.specimens:
        if specimen.number > highest:
            highest = specimen.number
    return highest
