/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import GenericRequestBtn from "./GenericRequestBtn";
import { PopUpMessage, httpClient } from "@tol/tol-ui";


interface Props {
  id: string,
  forceUpdate: boolean,
  setForceUpdate: any
}

function AcceptRequestBtn(props: Props) {
  const { id, forceUpdate, setForceUpdate } = props;

  const acceptRequest = () => {
    const json =[{'request_id': id}]
    httpClient().patch("/request/accept", json)
    .then(() => {
      PopUpMessage({
        type: "success",
        message: "Request accepted successfully.",
      })
      setForceUpdate(!forceUpdate);
    })
    .catch((error: any) => {
      PopUpMessage({
        type: "error",
        message: "Failed to accept request: " + error.message,
      })
    });
  }

  return (
    <>
      <GenericRequestBtn
        onClick={acceptRequest}
        variant="accept"
        text="Accept"
      />
    </>
  );
}

export default AcceptRequestBtn;