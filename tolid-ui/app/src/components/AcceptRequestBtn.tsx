/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import GenericRequestBtn from "./GenericRequestBtn";

function AcceptRequestBtn() {
  return <>
    <GenericRequestBtn
      onClick={() => void (0)}
      variant="accept"
      text="Accept"
    />
  </>;
}

export default AcceptRequestBtn;