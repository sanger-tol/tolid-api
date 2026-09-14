/*
SPDX-FileCopyrightText: 2026 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

/**
 * Values returned from the ToLID request form.
*/
export interface IRequestFormData {
  /** NCBI taxonomy identifier supplied by the user. */
  requestedTaxonomyId: string;
  /** Internal specimen identifier supplied by the user's lab. */
  specimenId: string;
}
