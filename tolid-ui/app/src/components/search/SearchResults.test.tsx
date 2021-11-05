/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import React from "react";
import { act } from "react-dom/test-utils";
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import SearchResults from "./SearchResults";

it("renders search data", async () => {
  const fakeResultsToLIDs = [
    {
      "species": {
        "commonName": "None",
        "family": "Nereididae",
        "genus": "Perinereis",
        "kingdom": "Metazoa",
        "order": "Phyllodocida",
        "phylum": "Annelida",
        "prefix": "wpPerVanc",
        "scientificName": "Perinereis vancaurica",
        "taxaClass": "Polychaeta",
        "taxonomyId": 6355,
    },
      "specimen": {
        "specimenId": "SAN0000200"
      },
      "tolId": "wpPerVanc1"
    }
  ];
  const fakeResultsSpeciess = [{
    "commonName": "lugworm",
    "family": "Arenicolidae",
    "genus": "Arenicola",
    "order": "None",
    "phylum": "Annelida",
    "kingdom": "Metazoa",
    "prefix": "wuAreMari",
    "scientificName": "Arenicola marina",
    "taxaClass": "Polychaeta",
    "taxonomyId": 6344,
    "tolIds": [
        {
            "specimen": {
                "specimenId": "SAN0000100"
            },
            "tolId": "wuAreMari1"
        },
        {
            "specimen": {
                "specimenId": "SAN0000101"
            },
            "tolId": "wuAreMari2"
        }
    ]
  }];
  const fakeResultsSpecimens = [
    {
      "specimenId": "SAN00001234",
      "tolIds": [
        {
          "species": {
            "commonName": "human",
            "family": "Hominidae",
            "genus": "Homo",
            "kingdom": "Metazoa",
            "order": "Primates",
            "phylum": "Chordata",
            "prefix": "mHomSap",
            "scientificName": "Homo sapiens",
            "taxaClass": "Mammalia",
            "taxonomyId": 9606,
          },
          "tolId": "mHomSap1"
        }
      ]
    }
  ];
  jest.spyOn(global, "fetch").mockImplementationOnce(() =>
      Promise.resolve({
      json: () => Promise.resolve(fakeResultsToLIDs),
      ok: true
    })
    ).mockImplementationOnce(() =>
      Promise.resolve({
      json: () => Promise.resolve(fakeResultsSpeciess),
      ok: true
    })
    ).mockImplementationOnce(() =>
      Promise.resolve({
      json: () => Promise.resolve(fakeResultsSpecimens),
      ok: true
    })
    );

  render(<SearchResults/>);
  // Use the asynchronous version of act to apply resolved promises
  await act(async () => {
    const input = screen.queryByRole('textbox')
    userEvent.type(input, 'good')
    const searchButton = screen.queryByRole('button')
    userEvent.click(searchButton)
  });

  // ToLID
  expect(screen.queryAllByText(new RegExp(fakeResultsToLIDs[0].tolId))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsToLIDs[0].species.taxonomyId))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsToLIDs[0].species.scientificName))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsToLIDs[0].specimen.specimenId))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsToLIDs[0].species.phylum))).toHaveLength(0);
  
  // Species
  expect(screen.queryAllByText(new RegExp(fakeResultsSpeciess[0].taxonomyId))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsSpeciess[0].tolIds[0].tolId))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsSpeciess[0].scientificName))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsSpeciess[0].tolIds[0].specimen.specimenId))).not.toHaveLength(0);
  
  // Specimen
  expect(screen.queryAllByText(new RegExp(fakeResultsSpecimens[0].specimenId))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsSpecimens[0].tolIds[0].tolId))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsSpecimens[0].tolIds[0].species.taxonomyId))).not.toHaveLength(0);
  expect(screen.queryAllByText(new RegExp(fakeResultsSpecimens[0].tolIds[0].species.scientificName))).not.toHaveLength(0);

  expect(screen.queryByText(/No results found/)).not.toBeInTheDocument(0);

  // remove the mock to ensure tests are completely isolated
  global.fetch.mockRestore();
});

it("renders search data", async () => {
  jest.spyOn(global, "fetch").mockImplementation(() =>
      Promise.resolve({
      json: () => Promise.resolve([]),
      ok: true
    })
    );

  render(<SearchResults/>);
  // Use the asynchronous version of act to apply resolved promises
  await act(async () => {
    const input = screen.queryByRole('textbox')
    userEvent.type(input, 'good')
    const searchButton = screen.queryByRole('button')
    userEvent.click(searchButton)
  });

  expect(screen.queryByText(/No results found/)).toBeInTheDocument(0);
    
  // remove the mock to ensure tests are completely isolated
  global.fetch.mockRestore();
});