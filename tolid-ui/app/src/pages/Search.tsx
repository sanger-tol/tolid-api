 /*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { RemoteTable, Widgets, env } from "@tol/tol-ui";

function Search() {
  const filter = {
    in_list: {},
    and_: {
      "tolid_specimen.id": {exists:{}},
      "tolid_species.id": {gt: {value: 0}}
    }
  };

  const table = (
    <RemoteTable
      id="tolid-table-v1"
      endpoint="tolid"
      noConfigModal
      noDownload
      filter={filter}
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
          rename: "Specimen",
          cellRenderer: null
        }
      }}
      baseUrl={env.TOL_DATA}
    />
  );

  const title = (
    <div>
      <h2>Search</h2>
      <p style={{marginTop: 4}}>
        Search on a ToLID prefix, taxonomy ID, species name or ToLID.
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

export default Search;
