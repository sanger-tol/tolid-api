/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { RemoteTable, Widgets, TsDataSource, useZone } from "@tol/tol-ui";
import { ActionButtons, DetailAttribute } from "../components";
import { useState } from "react";

function PendingRequests() {
  const [forceUpdate, setForceUpdate] = useState(false);

  const BoundActionButtons = (props: any) => (
    <ActionButtons
      {...props}
      forceUpdate={forceUpdate}
      setForceUpdate={setForceUpdate}
    />
  );

  const tolidZone = useZone({
    objectType: 'request',
    dataSource: new TsDataSource(),
    components: [{
      id: 'requests-table',
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
      id="requests-table"
      noDownload
      noConfigModal
      forceUpdate={forceUpdate}
      defaultSort="created_at"
      cellRenderers={{
        detailAttribute: DetailAttribute,
        actionButtons: BoundActionButtons,
      }}
      fields={{
        data: {
          species_id: {
            rename: "Taxon ID",
            sort: true,
            width: 100
          },
          status: {  // Not used
            rename: "Prefix",
            cellRenderer: {
              type: "detailAttribute",
              props: {
                id: "${species_id}",
                endpoint: 'species',
                attribute: 'prefix'
              }
            },
            sort: false,
            filter: false
          },
          requested_taxonomy_id: {
            rename: "Requested Taxon ID",
            sort: true
          },
          "user.id": {  // Not used
            rename: "Scientific Name",
            cellRenderer: {
              type: "detailAttribute",
              props: {
                id: "${~species_id}",
                endpoint: 'species',
                attribute: 'name',
              }
            },
            sort: false,
            filter: false
          },
          "user.email": {  // Not used
            rename: "Scientific Name (GOAT)",
            cellRenderer: {
              type: "detailAttribute",
              props: {
                id: "${~species_id}",
                endpoint: 'taxon',
                attribute: 'scientific_name'
              }
            },
            sort: false,
            filter: false
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
          "id": {
            rename: "Action",
            width: 184,
            custom: true,
            cellRenderer: {
              type: "actionButtons",
              props: {
                requestId: "${~id}",
                speciesId: "${~species_id}",
              }
            },
            sort: false, filter: false
          }
        },
        order: {
          active: [
            "species_id",
            "status",
            "requested_taxonomy_id",
            "user.id",
            "user.email",
            "confirmation_name",
            "specimen_id",
            "user.name",
            "id"
          ]
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
