 /*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { RemoteTable, Widgets, env, useZone } from "@tol/tol-ui";

function SearchSpecies() {
  const filter = {
    in_list: {},
    and_: {
      "tolid_genus": {exists:{}},
      "id": {gt: {value: 0}}
    }
  };

  const speciesZone = useZone({
    endpoint: 'species',
    components: [
      {
        id: 'species-table-v2',
        filter: filter
      }
    ],
    baseUrl: env.TOL_DATA
  });


  const table = (
    <RemoteTable
      id="species-table-v2"
      noConfigModal
      noDownload
      defaultSort="tolid_prefix"
      fields={{
        "uid": {
          rename: "Taxonomy ID"
        },
        "tolid_name": {
          rename: "Species Name"
        },
        "tolid_prefix": {
            rename: "ToLID Prefix",
            cellRenderer: null
          },
          "informatics_tolid_count": {
            rename: "No. ToLIDs Assigned",
            cellRenderer: null
          }
          }}
      {...speciesZone}
    />
  );

  const title = (
    <div>
      <h2>Search Species</h2>
      <p style={{marginTop: 4}}>
        Search for species in the ToLID database and view their ToLID prefix.
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

export default SearchSpecies;
