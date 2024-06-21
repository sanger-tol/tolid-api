/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { AcceptRequestBtn, AddSpeciesBtn, RejectRequestBtn } from "../components";

function PendingRequests() {
  return (
    <div className="container">
      <h1>Pending Requests</h1>
      <AddSpeciesBtn />
      <AcceptRequestBtn />
      <RejectRequestBtn />
    </div>
  );
}

export default PendingRequests;
