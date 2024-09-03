/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { RemoteTable, Widgets, useZone } from "@tol/tol-ui";
import { ActionButtons, DetailAttribute } from "../components";
import { useState } from "react";

function PendingRequests() {
  const [forceUpdate, setForceUpdate] = useState(false);

  const tolidZone = useZone({
    endpoint: 'request',
    components: [{
      id: 'requests-table-v1',
      filter: {
        and_: {
          'status': {
            in_list: {
              value: ['Pending'],
            }
          }
        }
      }
    }]
  });

  const table = (
    <RemoteTable
      id="requests-table-v1"
      noDownload
      noConfigModal
      forceUpdate={forceUpdate}
      defaultSort="created_at"
      fields={{
        species_id: {
          rename: "Taxon ID",
          sort: true,
          width: 100
        },
        custom_prefix: {
          rename: "Prefix",
          custom: true,
          cellRenderer: {
            element: DetailAttribute,
            propPointers: {
              id: 'species_id'
            },
            props: {
              endpoint: 'species',
              attribute: 'prefix'
            }
          },
          sort: false
        },
        requested_taxonomy_id: {
          rename: "Requested Taxon ID",
          sort: true
        },
        custom_scientific_name: {
          rename: "Scientific Name",
          custom: true,
          cellRenderer: {
            element: DetailAttribute,
            propPointers: {
              id: 'species_id'
            },
            props: {
              endpoint: 'species',
              attribute: 'name'
            }
          },
          sort: false
        },
        custom_scientific_name_goat: {
          rename: "Scientific Name (GOAT)",
          custom: true,
          cellRenderer: {
            element: DetailAttribute,
            propPointers: {
              id: 'species_id'
            },
            props: {
              endpoint: 'taxon',
              attribute: 'scientific_name'
            }
          },
          sort: false
        },
        confirmation_name: {
          rename: "Name Confirmation",
          sort: true
        },
        specimen_id: {
          rename: "Specimen ID",
          sort: true

        },
        "user.name": {
          rename: "Requester",
          sort: true
        },
        // next tolid
        custom_action: {
          rename: "Action",
          width: 184,
          custom: true,
          cellRenderer: {
            element: ActionButtons,
            propPointers: {
              requestId: 'id',
              speciesId: 'species_id'
            },
            props: {
              // @ts-ignore
              forceUpdate: forceUpdate,
              // @ts-ignore
              setForceUpdate: setForceUpdate
            }
          },
          sort: false
        }
      }}
      {...tolidZone}
    />
  );

  const title = (
    <div>
      <h2>Pending Requests</h2>
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
