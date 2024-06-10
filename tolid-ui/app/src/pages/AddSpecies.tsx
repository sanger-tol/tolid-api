/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { useState } from 'react';
import { Alert, Button, httpClient, Widgets } from '@tol/tol-ui';

const EMPTY_SPECIES_DATA_ERROR = "Species data cannot be an empty line.";
const WRONG_NUMBER_OF_ENTRIES_ERROR = "9 entries must be provided.";
const TAXONOMY_ID_INTEGER_ERROR = "Taxonomy ID (3rd entry) must be a number.";

function AddSpecies() {
  const [speciesData, setSpeciesData] = useState("");
  const [errorMessages, setErrorMessages] = useState<string[]>([]);
  const [success, setSuccess] = useState<string>("");
  const [errorMessagesAvailable, setErrorMessagesAvailable] = useState<boolean>(false);

  const speciesTitleArray = [
    "prefix",
    "name",
    "id",
    "common_name",
    "genus",
    "family",
    "tax_order",
    "tax_class",
    "phylum",
    "kingdom"
  ]

  function convertInputToJSONPayload() {
    const speciesValuesArray = splitLines(speciesData);

    if (speciesValuesArray[speciesValuesArray.length - 1] === "") {
      speciesValuesArray.pop();
    }

    const splitData = speciesValuesArray.map(line => splitLineToValues(line));

    const isValid: boolean = validateAllLines(splitData);
    if (!isValid) {
      setErrorMessagesAvailable(true);
      return null;
    }

    const data = splitData.map(split => convertLineToJSON(split));

    const dataArray: any[] = data.map(item => {
      const attributes = JSON.parse(item);
      const { id, ...attributesMinusId } = attributes;

      return {
        "attributes": attributesMinusId,
        "id": id,
        "type": "species",
      }
    });

    const payload = {
      "data": dataArray
    };

    return payload;
  }

  function splitLineToValues(line: string): string[] {
    const regEx = /\s+/;
    return [...line.split(regEx).filter(value => value !== ""), ""];
  }

  function splitLines(text: string): string[] {
    return text.split("\n");
  }

  function convertLineToJSON(line: string[]) {
    const JSONLine = speciesTitleArray.reduce((obj, key, index) => {
      obj[key] = line[index];
      return obj;
    }, {} as any);
    return JSON.stringify(JSONLine);
  }

  const postNewSpecies = (payload: any) => {
    httpClient().post('/species:upsert', payload)
      .then(() => {
        setSuccess("Success!");
      }).catch(() => {
        setErrorMessagesAvailable(true);
        setSuccess("Request unsuccessful, please check your data and try again.");
      });
  }

  function resetErrors() {
    setErrorMessages([]);
    setErrorMessagesAvailable(false);
    setSuccess("");
  }

  function validateNonEmptyTextArea(array: string[]): boolean {
    if (array[0].trim().length === 0 || array === undefined) {
      setErrorMessages(previousErrorMessages => [
        ...previousErrorMessages, `${EMPTY_SPECIES_DATA_ERROR}`
      ]);
      return false;
    }
    return true;
  }

  function validateIndividualLines(array: string[], lineNumber: number): boolean {
    if (array.length != 10) {
      setErrorMessages(previousErrorMessages => [
        ...previousErrorMessages, `Line ${lineNumber}: ${WRONG_NUMBER_OF_ENTRIES_ERROR}`
      ]);
      return false;
    }
    return true;
  }

  function validateTaxonomyId(array: string[], lineNumber: number): boolean {
    if (array[2] !== undefined && !Number.isInteger(parseInt(array[2].trim()))) {
      setErrorMessages(previousErrorMessages => [
        ...previousErrorMessages, `Line ${lineNumber}: ${TAXONOMY_ID_INTEGER_ERROR}`
      ]);
      return false;
    }
    return true;
  }

  function validateAllLines(data: string[][]) {
    resetErrors();

    let allValid = true;

    data.forEach((line, index) => {
      const lineNumber = index + 1;
      const nonEmptyValid = validateNonEmptyTextArea(line);
      const individualLinesValid = validateIndividualLines(line, lineNumber);
      const taxonomyIdValid = validateTaxonomyId(line, lineNumber);

      if (!nonEmptyValid || !individualLinesValid || !taxonomyIdValid) {
        allValid = false;
      }
    });

    if (!allValid) {
      setErrorMessagesAvailable(true);
    }

    return allValid;
  }

  const title = (
    <div>
      <h2>Add Species</h2>
    </div>
  );

  const errors = errorMessages.map((message) => {
    return (
      <div className="add-species-error-wrapper">
        <Alert
          type='error'
          message={message}
        />
      </div>
    );
  });

  const addSpeciesForm = (
    <div className="add-species-wrapper">
      <div>
        <p>Add species data below:</p>
        <textarea
          className="add-species-textarea"
          value={speciesData}
          onChange={(e) => {
            setSpeciesData(e.target.value);
            resetErrors();
          }}
          placeholder='Enter species data here...'
        />
      </div>
      <div>
        {success !== "" && (
          <p style={{ fontSize: "14px" }}>{success}</p>
        )}
      </div>
      <div className="add-species-button-wrapper">
        <Button disabled={speciesData === "" || errorMessagesAvailable === true} variant={(speciesData === "" || errorMessagesAvailable === true) ? "" : "success"}
          onClick={() => {
            postNewSpecies(convertInputToJSONPayload());
          }}>
          Submit
        </Button>
      </div>
      {errors}
    </div>
  );

  const components = [
    {
      component: title,
      type: 'full'
    },
    {
      component: addSpeciesForm,
      type: 'full'
    }
  ]

  return (
    <>
      <Widgets
        components={components}
      />
    </>
  );
}

export default AddSpecies;
