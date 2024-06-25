/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { RemoteTable, Widgets, useZone } from "@tol/tol-ui";
import { ActionButtons, SpeciesName, SpeciesTaxon } from "../components";

function PendingRequests() {
  const tolidZone = useZone({
    endpoint: 'request',
    baseUrl: '/api/v3',
    components: [{
      id: 'requests-table-v1',
      /*
      filter: {
        and_: {
          'status': {
            in_list: {
              value: ['Accepted', 'Rejected'],
              negate: true
            }
          }
        }
      }
      */
    }]
  });

  const table = (
    <RemoteTable
      id="requests-table-v1"
      //noConfigModal
      noFilter
      noDownload
      fields={{
        id: {
          rename: "Request ID",
          sort: false,
          width: 100
        },
        custom_taxon: {
          rename: "Taxon ID",
          cellRenderer: {
            element: SpeciesTaxon,
            propPointers: {
              id: 'species_id'
            }
          },
          sort: false,
          width: 100
        },
        custom_scientific_name: {
          rename: "Scientific Name",
          cellRenderer: {
            element: SpeciesName,
            propPointers: {
              id: 'species_id'
            }
          },
          sort: false
        },
        confirmation_name: {
          rename: "Name Confirmation",
          sort: false
        },
        specimen_id: {
          rename: "Specimen ID",
          sort: false

        },
        "user.name": {
          rename: "Requester",
          sort: false
        },
        // next tolid
        custom_action: {
          rename: "Action",
          width: 184,
          cellRenderer: {
            element: ActionButtons,
            propPointers: {
              requestId: 'id',
              speciesId: 'species_id'
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
