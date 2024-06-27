/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import GenericRequestBtn from "./GenericRequestBtn";
// import { httpClient } from "@tol/tol-ui";


interface Props {
  id: string
}

function AcceptRequestBtn(props: Props) {
  const { id } = props;

  const acceptRequest = () => {
    console.log(id);
  }

  return (
    <GenericRequestBtn
      onClick={acceptRequest}
      variant="accept"
      text="Accept"
    />
  );
}

export default AcceptRequestBtn;