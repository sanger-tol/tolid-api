/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { useState } from 'react';
import { Modal, Button } from '@tol/tol-ui';
import { Form, Radio, RadioGroup, Input } from 'rsuite';
import GenericRequestBtn from './GenericRequestBtn';


interface Props {
  id: string
}

function RejectRequestBtn(props: Props) {
  const { id } = props;
  const [open, setOpen] = useState(false);
  const [rejectionChoice, setRejectionChoice] = useState("");
  const [rejectionReason, setRejectionReason] = useState("");
  const TAXON_NOT_SPECIES_LEVEL = "Taxonomy ID is not species-level";

  const openModal = () => {
    setOpen(!open);
  };

  const rejectModalButton = (
    <Button
      onClick={() => {
        openModal();
      }}
      variant="danger"
      style={{height: 30, padding: "0 10px"}}
    >
      Reject Request
    </Button>
  );

  return (
    <>
      <GenericRequestBtn
        onClick={() => {
          openModal();
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