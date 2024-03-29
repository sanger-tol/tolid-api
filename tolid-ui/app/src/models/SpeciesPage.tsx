/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Species } from "./Species";

export interface SpeciesPage {
    species: Species[];
    totalNumSpecies: number;
}
