/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { RemoteTable, Widgets, useZone } from "@tol/tol-ui";

function PendingRequests() {
  const tolidZone = useZone({
    endpoint: 'request',
    baseUrl: '/api/v3',
    components: [{id: 'requests-table-v1'}]
  });


  const table = (
    <RemoteTable
      id="requests-table-v1"
      noConfigModal
      noDownload
      fields={{
        id: {
          rename: "Request ID",
          filterType: 'str'
        },
        // taxon_id
        // scientific_name
        confirmation_name: {
          rename: "Name Confirmation",
          filterType: 'str'
        },
        specimen_id: {
          rename: "Specimen ID",
          filterType: 'str'
        },
        "user.name": {
          rename: "Requester",
          filterType: 'str'
        }
        // next tolid
        // action
      }}
      {...tolidZone}
    />
  );

  const title = (
    <div>
      <h2>Pending Requests</h2>
      <p style={{marginTop: 4}}>
        Text here...
      </p>
    </div>
  );

  const components = [
    {
      component: title,
      type: 'full'
    },
    {
      component: table,
      type: 'xl'
    }
  ];

  return (
    <div className="search">
      <Widgets
        components={components}
      />
    </div>
  );
}

export default PendingRequests;
