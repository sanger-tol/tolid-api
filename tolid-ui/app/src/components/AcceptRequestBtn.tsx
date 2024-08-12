/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { useState } from "react";
import GenericRequestBtn from "./GenericRequestBtn";
import { PopUpMessage, httpClient } from "@tol/tol-ui";


interface Props {
  id: string,
  forceUpdate: boolean,
  setForceUpdate: any
}

function AcceptRequestBtn(props: Props) {
  const { id, forceUpdate, setForceUpdate } = props;
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const acceptRequest = () => {
    const json =[{'request_id': id}]
    httpClient().patch("/request/accept", json)
    .then(() => {
      setSuccessMessage("Request accepted successfully.");
      setForceUpdate(!forceUpdate);
    })
    .catch((error: any) => {
      setErrorMessage("Failed to accept request: " + error.message);
    });
  }

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
        onClick={acceptRequest}
        variant="accept"
        text="Accept"
      />
    </>
  );
}

export default AcceptRequestBtn;