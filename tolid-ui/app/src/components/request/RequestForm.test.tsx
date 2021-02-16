import React from "react";
import { act } from "react-dom/test-utils";
import { render, screen, prettyDOM } from '@testing-library/react';
import userEvent from '@testing-library/user-event'
import RequestForm from "./RequestForm";

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
      "id": "1",
      "status": "Pending",
      "createdBy": {
        "email": "user@example.com",
        "name": "A User",
        "organisation": "Research Inc"
      }
    }
  ];

  jest.spyOn(global, "fetch").mockImplementationOnce(() =>
      Promise.resolve({
      json: () => Promise.resolve(fakeResults),
      ok: true
    })
    );

  render(<RequestForm/>);
  // Use the asynchronous version of act to apply resolved promises
  await act(async () => {
    const inputTax = screen.queryByPlaceholderText('NCBI Taxonomy ID')
    userEvent.type(inputTax, '6355')
    const inputSpec = screen.queryByPlaceholderText('Specimen ID')
    userEvent.type(inputSpec, 'SAN0000200')
    const requestButton = screen.queryByRole('button')
    userEvent.click(requestButton)
  });
  expect(screen.queryByText(/has been requested/i)).toBeInTheDocument();

  // remove the mock to ensure tests are completely isolated
  global.fetch.mockRestore();
});

it("failed request", async () => {
  const fakeResults = {
      "detail": "You cannot do that"
  };

  jest.spyOn(global, "fetch").mockImplementationOnce(() =>
      Promise.resolve({
      json: () => Promise.resolve(fakeResults),
      ok: true
    })
    );

  render(<RequestForm/>);
  // Use the asynchronous version of act to apply resolved promises
  await act(async () => {
    const inputTax = screen.queryByPlaceholderText('NCBI Taxonomy ID')
    userEvent.type(inputTax, '6355')
    const inputSpec = screen.queryByPlaceholderText('Specimen ID')
    userEvent.type(inputSpec, 'SAN0000200')
    const requestButton = screen.queryByRole('button')
    userEvent.click(requestButton)
  });
  expect(screen.queryByText(/cannot do that/i)).toBeInTheDocument();

  // remove the mock to ensure tests are completely isolated
  global.fetch.mockRestore();
});