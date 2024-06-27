/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { useState } from "react";
import {
  AcceptRequestBtn,
  AddSpeciesBtn,
  RejectRequestBtn,
  fetchDetail
} from "../components";
import { Loader } from "@tol/tol-ui";


interface Props {
  requestId: any,
  speciesId: any,
  forceUpdate: boolean,
  setForceUpdate: any
}

function ActionButtons(props: Props) {
  const { requestId, speciesId, forceUpdate, setForceUpdate } = props;
  const [loading, setLoading] = useState(true);
  const [canAccept, setCanAccept] = useState(false);

  fetchDetail(speciesId, 'species').then((res: any) => {
    if ('data' in res && 'id' in res.data.data) {
      setCanAccept(true);
    }
    setLoading(false);
  });

  return (
    <div className="loading-cell">
      {loading ?
        <Loader
          size="sm"
          role="status"
          aria-hidden
        />
      :
        <div className="action-buttons">
          {canAccept ? (
            <AcceptRequestBtn
              id={requestId}
            />
          ) : (
            <AddSpeciesBtn />
          )}
          <RejectRequestBtn
            id={requestId}
            forceUpdate={forceUpdate}
            setForceUpdate={setForceUpdate}
          />
        </div>
      }
    </div>
  );
}

export default ActionButtons;
