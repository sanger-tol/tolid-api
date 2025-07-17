/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { useEffect, useState } from "react";
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
  const { requestId, speciesId, forceUpdate } = props;
  const [loading, setLoading] = useState(true);
  const [canAccept, setCanAccept] = useState(false);

  useEffect (() => {
    fetchDetail(speciesId, 'species').then((res: any) => {
      setCanAccept('data' in res && 'id' in res.data.data);
      setLoading(false);
    });
  }, [forceUpdate, speciesId]);

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
              {...props}
            />
          ) : (
            <AddSpeciesBtn />
          )}
          <RejectRequestBtn
            id={requestId}
            {...props}
          />
        </div>
      }
    </div>
  );
}

export default ActionButtons;
