/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import {
  Button,
  Form,
  Modal,
  PopUpMessage,
  Status,
  Widgets,
  httpClient
} from '@tol/tol-ui';
import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';


function Profile() {
  const [requestedTaxonomyId, setRequestedTaxonomyId] = useState("");
  const [specimenId, setSpecimenId] = useState("");

  const [speciesTaxonomyId, setSpeciesTaxonomyId] = useState("");
  const [speciesName, setSpeciesName] = useState("");

  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);

  const clearAll = () => {
    setRequestedTaxonomyId("");
    setSpecimenId("");
    setSpeciesTaxonomyId("");
    setSpeciesName("");
  }

  const openModal = () => {
    setOpen(true);
    setSuccess("");
    setError("");
  };

  const getTolidTaxonInfo = () => {
    setSpeciesTaxonomyId("");
    setSpeciesName("");
    httpClient().get('/species/' + requestedTaxonomyId, {})
    .then((res: any) => {
      const data = res.data.data;
      setSpeciesTaxonomyId(data?.id || '');
      setSpeciesName(data?.attributes?.name || '');
      openModal();
    }).catch(() => {
      getGoatTaxonInfo();
    });
  };

  const getGoatTaxonInfo = () => {
    let newSpeciesTaxonomyId = "";
    httpClient().get('/taxon/' + requestedTaxonomyId, {})
    .then((res: any) => {
      const relationships = res.data.data.relationships;
      newSpeciesTaxonomyId = relationships?.species?.data?.id || '';
      setSpeciesTaxonomyId(newSpeciesTaxonomyId);
      setSpeciesName(relationships?.species?.data?.attributes?.scientific_name || '');
    })
    .catch(() => {})
    .finally(() => {
      if (newSpeciesTaxonomyId === "") {
        setError("The Taxonomy ID cannot be found in GoaT or is above species level")
      } else {
        openModal();
      }
    });
  }

  const saveRequest = () => {
    setOpen(false);
    clearAll();
    setSuccess("ToLID request submitted successfully");
  }

  const requestButton = (
    <Button variant="success" onClick={saveRequest}>
      <strong style={{marginRight: 4}}>Request</strong>
      <FontAwesomeIcon icon={faArrowRight} size="sm" />
    </Button>
  );

  const createRequest = (
    <div>
      <h2 className="sub-heading">Request a ToLID</h2>
      <Form>
        <Form.Group>
          <Form.Control
            value={requestedTaxonomyId}
            onChange={(e) => setRequestedTaxonomyId(e.target.value)}
            placeholder="NCBI Taxonomy ID"
          />
          <p className="form-info">The Taxonomy ID as registered at NCBI. This must be a species-level taxonomy ID.</p>
          <Form.Control
            value={specimenId}
            onChange={(e) => setSpecimenId(e.target.value)}
            id="specimenId"
            placeholder="Specimen ID"
          />
          <p className="form-info">The internal ID of the specimen. This is only used in the ToLID system and should be how you refer to the specimen in your lab</p>
        </Form.Group>
        <Button disabled={requestedTaxonomyId === "" || specimenId === ""} onClick={() => getTolidTaxonInfo()}>
          Request
        </Button>
      </Form>
      <Modal
        size='md'
        open={open}
        setOpen={setOpen}
        actionButton={requestButton}
      >
        <h2>Confirm ToLID Request</h2>
        <>{requestedTaxonomyId !== speciesTaxonomyId &&
          <Status
            status="warning"
            text={"The requested Taxonomy ID is not species level. The generated ToLID will be for the species: " + speciesName}
          />
        }</>
        <h5 style={{marginTop: 12, marginBottom: 10}}>Are you sure you want to request a ToLID for the following species?</h5>
        <p><strong>Requested Taxonomy ID: </strong><span className='request-value'>{requestedTaxonomyId}</span></p>
        <p><strong>Species Level Taxonomy ID: </strong><span className="request-value">{speciesTaxonomyId}</span></p>
        <p><strong>Species Level Scientific Name: </strong><span className="request-value">{speciesName}</span></p>
        <p><strong>Specimen ID: </strong><span className="request-value">{specimenId}</span></p>
      </Modal>
    </div>
  );

  const myTolids = (
    <div>
      <h2 className="sub-heading">My ToLIDs</h2>
    </div>
  );

  const listRequests = (
    <div>
      <h2 className="sub-heading">My Requests</h2>
    </div>
  );

  const components = [
    {
      component: createRequest,
      type: 'full'
    },
    {
      component: myTolids,
      type: 'full'
    },
    {
      component: listRequests,
      type: 'full'
    }
  ];

  return (
    <div className="profile">
      <PopUpMessage
        type='success'
        message={success}
        setMessage={setSuccess}
      />
      <PopUpMessage
        type='danger'
        message={error}
        setMessage={setError}
      />
      <Widgets
        components={components}
      />
    </div>
  );
}

export default Profile;
