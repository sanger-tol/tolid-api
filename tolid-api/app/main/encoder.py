# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

from json import JSONEncoder

from main.model import Base


class JSONEncoder(JSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Base):
            return o.to_dict()
        return JSONEncoder.default(self, o)
