/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { useState } from 'react';
import { Modal, Button, PopUpMessage, httpClient } from '@tol/tol-ui';
import { Form, Radio, RadioGroup, Input } from 'rsuite';
import GenericRequestBtn from './GenericRequestBtn';


interface Props {
  id: string,
  forceUpdate: boolean,
  setForceUpdate: any
}

function RejectRequestBtn(props: Props) {
  const { id, forceUpdate, setForceUpdate } = props;
  const [open, setOpen] = useState(false);
  const [rejectionChoice, setRejectionChoice] = useState("");
  const [rejectionReason, setRejectionReason] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const TAXON_NOT_SPECIES_LEVEL = "Taxonomy ID is not species-level";

  const setRemoteRejection = () => {
    const upsertData = {
      data: [{
        id: id,
        type: "request",
        attributes: {
          status: "Rejected",
          reason: rejectionReason ? rejectionReason : null
        }
      }]
    }
    httpClient().post("/request:upsert", upsertData)
    .then(() => {
      setSuccessMessage("Request rejected successfully.");
      setForceUpdate(!forceUpdate);
    })
    .catch((error: any) => {
      setErrorMessage("Failed to reject request: " + error.message);
    });
  }

  const rejectModalButton = (
    <Button
      onClick={() => {
        setOpen(false);
        setRemoteRejection();
      }}
      variant="danger"
      style={{height: 30, padding: "0 10px"}}
    >
      Reject Request
    </Button>
  );

  return (
    <>
      <PopUpMessage
        type='success'
        message={successMessage}
        setMessage={setSuccessMessage}
      />
      <PopUpMessage
        type='danger'
        message={errorMessage}
        setMessage={setErrorMessage}
      />
      <GenericRequestBtn
        onClick={() => {
          setOpen(true);
          setRejectionReason("");
          setRejectionChoice("");
        }}
        variant="reject"
        text="Reject"
      />
      <Modal
        size="md"
        open={open}
        setOpen={setOpen}
        actionButton={rejectModalButton}
      >
        <h3>Request {id} rejection reason</h3>
        <p style={{ marginTop: "10px", marginBottom: "10px" }}>Note: A rejection reason is not required.</p>
        <Form fluid style={{ marginTop: "20px auto" }}>
          <Form.Group>
            <RadioGroup
              name="radioList"
              inline
              // @ts-ignore
              onChange={setRejectionChoice}
            >
              <Radio
                value={TAXON_NOT_SPECIES_LEVEL}
                onChange={() => setRejectionReason(TAXON_NOT_SPECIES_LEVEL)}
              >
                Taxonomy ID is not species-level
              </Radio>
              <Radio
                value="custom"
                onChange={() => setRejectionReason("")}
              >
                Custom
              </Radio>
            </RadioGroup>
          </Form.Group>
          {rejectionChoice === "custom" &&
            <Form.Group>
              <Input
                value={rejectionReason}
                placeholder="Custom rejection reason"
                onChange={setRejectionReason}
              />
            </Form.Group>
          }
        </Form>
      </Modal>
    </>
  )
}

export default RejectRequestBtn;