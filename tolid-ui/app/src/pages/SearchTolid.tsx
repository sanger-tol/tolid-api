 /*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { RemoteTable, Widgets, env, useZone } from "@tol/tol-ui";

function SearchTolid() {
  const filter = {
    in_list: {},
    and_: {
      "tolid_species.id": {gt: {value: 0}}
    }
  };

  const tolidZone = useZone({
    endpoint: 'tolid',
    components: [
      {
        id: 'tolid-table-v6',
        filter: filter
      }
    ],
    baseUrl: env.TOL_DATA
  });


  const table = (
    <RemoteTable
      id="tolid-table-v6"
      noConfigModal
      noDownload
      fields={{
        "uid": {
          rename: "ToLID"
        },
        "tolid_species.tolid_name": {
          rename: "Species Name"
        },
        "tolid_species.id": {
          rename: "Taxonomy ID",
          cellRenderer: null
        },
        "tolid_specimen.id": {
          rename: "Specimen ID",
          cellRenderer: null
        }
      }}
      {...tolidZone}
    />
  );

  const title = (
    <div>
      <h2>Search ToLIDs</h2>
      <p style={{marginTop: 4}}>
        Search for assigned ToLIDs. Results will only be shown here for species that have had ToLIDs assigned.
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

export default SearchTolid;
