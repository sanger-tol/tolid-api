{/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/}

import { Species } from './Species';
import { Specimen } from './Specimen';

export interface ToLID {
  species: Species;
  specimen: Specimen;
  tolId: string;
}

