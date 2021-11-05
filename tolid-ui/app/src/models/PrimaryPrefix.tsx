{/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/}

import { SecondaryPrefix } from './SecondaryPrefix';

export interface PrimaryPrefix {
    letter: string;
    name: string;
    secondaryPrefixes: SecondaryPrefix[];
}
