/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

const ADD_ID = "NEED TO ADD ID HERE";

import { useState } from 'react';
import { Modal, Button } from '@tol/tol-ui';
import { Form, Radio, RadioGroup, Input } from 'rsuite';
import GenericRequestBtn from './GenericRequestBtn';

function RejectRequestBtn() {
  const [open, setOpen] = useState(false);
  const [rejectionReason, setRejectionReason] = useState("");
  const [customRejection, setCustomRejection] = useState("");

  const openModal = () => {
    setOpen(!open);
  };

  const rejectModalButton = (
    <Button
      onClick={() => {
        openModal();
        console.log(rejectionReason === "custom" ? customRejection : rejectionReason);
      }}
      variant="danger"
    >
      Reject Request
    </Button>
  );

  const handleRejection = (value: string) => {
    setRejectionReason(value);
  };

  const handleCustomRejection = (value: string) => {
    setCustomRejection(value);
  };

  const handleNoRejectionInput = () => {
    if (rejectionReason === "" && customRejection === "") {
      setRejectionReason("No rejection reason provided.");
    }
  }

  return (
    <>
      <GenericRequestBtn
        onClick={() => {
          openModal();
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
        <h3>Reason for rejection (ID: {ADD_ID})</h3>
        <p style={{ marginTop: "10px", marginBottom: "10px" }}>Note: A rejection reason is not required.</p>
        <Form fluid style={{ marginTop: "20px auto" }}>
          <Form.Group>
            <RadioGroup
              name="radioList"
              inline
              onChange={handleRejection}
            >
              <Radio
                onChange={() => setCustomRejection("")}
                value="Taxonomy ID is not species-level">
                Taxonomy ID is not species-level
              </Radio>
              <Radio value="custom">Custom</Radio>
            </RadioGroup>
          </Form.Group>
          <Form.Group>
            <Input
              value={customRejection}
              placeholder="Custom rejection reason"
              disabled={rejectionReason !== "custom"}
              onChange={handleCustomRejection}
              onClick={() => {
                handleRejection("custom");
              }}
            />
          </Form.Group>
        </Form>
      </Modal>
    </>
  )
}

export default RejectRequestBtn;