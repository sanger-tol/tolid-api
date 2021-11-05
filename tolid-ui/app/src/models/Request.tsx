{/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/}

import { Species } from './Species';
import { Specimen } from './Specimen';
import { User } from './User';

export interface Request {
  requestId: number;
  status: string;
  reason: string;
  createdBy: User;
  species: Species;
  specimen: Specimen;
  confirmationName?: string;
  synonyms?: string[];
}
