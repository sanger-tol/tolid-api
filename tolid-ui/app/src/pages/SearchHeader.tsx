/*
 * SPDX-FileCopyrightText: 2025 Genome Research Ltd.
 *
 * SPDX-License-Identifier: MIT
 */

import {
  StaticMessage,
} from "@tol/tol-ui";


export function SearchHeader() {

  const WarningMessage = (
    <div style={{ marginTop: 12 }}>
      <StaticMessage
        message={
          `Please note it can take 24 hours for new ToLIDs to appear in the search results`
        }
        type={"warning"}
      />
    </div>
  );

  return (
      <div className="search-header">
        {WarningMessage}
      </div>
  );
}
