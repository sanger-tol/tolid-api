/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { useState } from 'react';
import { Button, httpClient, PopUpMessage, Widgets, Status } from '@tol/tol-ui';
import { Input } from 'rsuite';

const EMPTY_SPECIES_DATA_ERROR = "Species data cannot be an empty line.";
const WRONG_NUMBER_OF_ENTRIES_ERROR = "9 entries must be provided.";
const TAXONOMY_ID_INTEGER_ERROR = "Taxonomy ID (3rd entry) must be a number.";
const REQUEST_UNSUCCESSFUL = "Request unsuccessful, errors have been highlighted below.";
const REQUEST_SUCCESSFUL = "Request successful, species has been added.";

function AddSpecies() {
  const [speciesData, setSpeciesData] = useState("");
  const [errorMessages, setErrorMessages] = useState<string[]>([]);
  const [success, setSuccess] = useState<string>("");
  const [failure, setFailure] = useState<string>("");
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

  const convertInputToJSONPayload = () => {
    const speciesValuesArray = splitLines(speciesData);

    if (speciesValuesArray[speciesValuesArray.length - 1] === "") {
      speciesValuesArray.pop();
    }

    const splitData = speciesValuesArray.map(line => splitLineToValues(line));
    console.log(splitData);
    const isValid = validateAllLines(splitData);

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

  const splitLineToValues = (line: string): string[] => {
    const regEx = /[\t]/;
    return [...line.split(regEx).filter(value => value !== ""), ""];
  }

  const splitLines = (text: string): string[] => {
    return text.split("\n");
  }

  const convertLineToJSON = (line: string[]) => {
    const JSONLine = speciesTitleArray.reduce((obj, key, index) => {
      obj[key] = line[index];
      return obj;
    }, {} as any);
    return JSON.stringify(JSONLine);
  }

  const postNewSpecies = (payload: any) => {
    httpClient().post('/species:upsert', payload)
      .then(() => {
        setSuccess(REQUEST_SUCCESSFUL);
        setSpeciesData("");
      }).catch(() => {
        setErrorMessagesAvailable(true);
        setErrorMessages(previousErrorMessages => [
          ...previousErrorMessages, `Could not submit, please check your data and try again.`
        ]);
        setFailure(REQUEST_UNSUCCESSFUL);
      });
  }

  const resetErrors = () => {
    setErrorMessages([]);
    setErrorMessagesAvailable(false);
    setSuccess("");
    setFailure("");
  }

  const validateNonEmptyTextArea = (array: string[]): boolean => {
    if (array[0].trim().length === 0 || array === undefined) {
      setErrorMessages(previousErrorMessages => [
        ...previousErrorMessages, `${EMPTY_SPECIES_DATA_ERROR}`
      ]);
      return false;
    }
    return true;
  }

  const validateIndividualLines = (array: string[], lineNumber: number): boolean => {
    if (array.length !== 10) {
      setErrorMessages(previousErrorMessages => [
        ...previousErrorMessages, `Line ${lineNumber}: ${WRONG_NUMBER_OF_ENTRIES_ERROR}`
      ]);
      return false;
    }
    return true;
  }

  const validateTaxonomyId = (array: string[], lineNumber: number): boolean => {
    if (array[2] !== undefined && !Number.isInteger(parseInt(array[2].trim()))) {
      setErrorMessages(previousErrorMessages => [
        ...previousErrorMessages, `Line ${lineNumber}: ${TAXONOMY_ID_INTEGER_ERROR}`
      ]);
      return false;
    }
    return true;
  }

  const validateAllLines = (data: string[][]) => {
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
      <h2 className="sub-heading">Add Species</h2>
      <p>Add species data below to be added to the database</p>
    </div>
  );

  const errors = errorMessages.map((message) => {
    return (
      <div className="add-species-alert-wrapper">
        <Status
          text={message}
          status="danger"
        />
      </div>
    );
  });

  const addSpeciesForm = (
    <div className="add-species-wrapper">
      <div>
        <p>Add species data below:</p>
        <Input
          as="textarea"
          className="add-species-textarea"
          value={speciesData}
          onChange={(value: any) => {
            setSpeciesData(value);
            resetErrors();
          }}
          placeholder='Enter species data here...'
        />
      </div>

      <div className="add-species-button-wrapper">
        <div className="errors-wrapper">
          {errors}
        </div>
        <div>
          <Button
            disabled={speciesData === "" || errorMessagesAvailable === true}
            variant={"success"}
            onClick={() => {
              postNewSpecies(convertInputToJSONPayload());
            }}>
            Submit
          </Button>
        </div>
      </div>
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
      <PopUpMessage
        type='success'
        message={success}
        setMessage={setSuccess}
      />
      <PopUpMessage
        type='danger'
        message={failure}
        setMessage={setFailure}
      />
      <Widgets
        components={components}
      />
    </>
  );
}

export default AddSpecies;
