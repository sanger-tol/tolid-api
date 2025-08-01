 /*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import {
  RemoteTable,
  Widgets,
  useZone,
  TOL_DS
} from "@tol/tol-ui";
import { SearchHeader } from "./SearchHeader";

function SearchTolid() {
  const Header = (
    <SearchHeader />
  );

  const filter = {
    in_list: {},
    and_: {
      "tolid_species.id": {gt: {value: 0}}
    }
  };

  const tolidZone = useZone({
    objectType: 'tolid',
    dataSource: TOL_DS,
    components: [
      {
        id: 'tolid-table',
        filter: filter
      }
    ]
  });


  const table = (
    <RemoteTable
      id="tolid-table"
      noConfigModal
      noDownload
      fields={{
        "id": {
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
      component: Header,
      type: 'full'
    },
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
