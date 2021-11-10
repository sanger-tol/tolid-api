/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { ToLID } from './ToLID';

export interface Species {
  commonName: string;
  family: string;
  genus: string;
  kingdom: string;
  order: string;
  phylum: string;
  prefix: string;
  scientificName: string;
  taxaClass: string;
  taxonomyId: number;
  currentHighestTolidNumber: number;
  tolIds: ToLID[];
}
