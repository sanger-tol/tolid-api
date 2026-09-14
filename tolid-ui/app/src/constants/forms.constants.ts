/*
SPDX-FileCopyrightText: 2026 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import type { IFormConfig } from "@tol/tol-ui";

export const REQUEST_FORM_CONFIG: IFormConfig = {
  fields: [
    {
      name: "requestedTaxonomyId",
      type: "text",
      label: "NCBI Taxonomy ID",
      placeholder: "NCBI Taxonomy ID",
      helpText: "The Taxonomy ID as registered at NCBI. This must be a species-level taxonomy ID.",
      required: true,
    },
    {
      name: "specimenId",
      type: "text",
      label: "Specimen ID",
      placeholder: "Specimen ID",
      helpText: (
        "The internal ID of the specimen. " +
        "This is only used in the ToLID system and should be how you refer to the specimen in your lab"
      ),
      required: true,
    },
  ],
  buttonConfig: {
    buttons: [{
      text: "Request",
    }],
  },
};
