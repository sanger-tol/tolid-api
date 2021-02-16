import React from "react";
import { act } from "react-dom/test-utils";
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import UserToLIDsList from "./UserToLIDsList";

it("successful request", async () => {
  const fakeResults = [
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

  jest.spyOn(global, "fetch").mockImplementationOnce(() =>
      Promise.resolve({
      json: () => Promise.resolve(fakeResults),
      ok: true
    }));

  render(<UserToLIDsList/>);
  expect(await screen.findByText(/Perinereis vancaurica/i)).toBeInTheDocument();
  expect(global.fetch).toHaveBeenCalledWith('/api/v2/tol-ids/mine', {"headers": {"Content-Type": "application/json", "api-key": "1234"}, "method": "GET"});

  // remove the mock to ensure tests are completely isolated
  global.fetch.mockRestore();
});

it("failed request", async () => {
  const fakeResults = {
      "detail": "You cannot do that",
      "title": "Error"
  };

  jest.spyOn(global, "fetch").mockImplementationOnce(() =>
      Promise.resolve({
      json: () => Promise.resolve(fakeResults),
      ok: false
    })
    );

  render(<UserToLIDsList/>);
  // Use the asynchronous version of act to apply resolved promises

  expect(await screen.findByText(/cannot do that/i)).toBeInTheDocument();
  expect(global.fetch).toHaveBeenCalledWith('/api/v2/tol-ids/mine', {"headers": {"Content-Type": "application/json", "api-key": "1234"}, "method": "GET"});
  // remove the mock to ensure tests are completely isolated
  global.fetch.mockRestore();
});