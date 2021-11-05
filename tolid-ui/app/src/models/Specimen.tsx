/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { ToLID } from './ToLID';

export interface Specimen {
    specimenId: string;
    tolIds: ToLID[];
}
  
  