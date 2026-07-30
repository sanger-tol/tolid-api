/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import {
  Button,
  Form,
  Modal,
  PopUpMessage,
  RemoteTable,
  StatusMessage,
  Widgets,
  httpClient,
  useZone,
  TsDataSource,
  TMessageType,
} from '@tol/tol-ui';
import { useState } from 'react';
import { DetailAttribute, TolidStatus } from "../components";
import { SubspeciesCellRenderer } from '../components'


function MyTolids() {
  const user = localStorage.getItem('user') || '{}';
  const userId = JSON.parse(user).id;
  const [requestedTaxonomyId, setRequestedTaxonomyId] = useState("");
  const [specimenId, setSpecimenId] = useState("");

  const [speciesTaxonomyId, setSpeciesTaxonomyId] = useState("");
  const [speciesName, setSpeciesName] = useState("");

  const [open, setOpen] = useState(false);
  const [forceUpdate, setForceUpdate] = useState(false);

  const clearAll = () => {
    setRequestedTaxonomyId("");
    setSpecimenId("");
    setSpeciesTaxonomyId("");
    setSpeciesName("");
  }

  const openModal = () => {
    setOpen(true);
  };

  const getTolidTaxonInfo = () => {
    setSpeciesTaxonomyId("");
    setSpeciesName("");
    httpClient().get('/species/' + requestedTaxonomyId, {})
    .then((res: any) => {
      const data = res.data.data;
      setSpeciesTaxonomyId(data?.id || '');
      setSpeciesName(data?.attributes?.name || '');
      openModal();
    }).catch(() => {
      getGoatTaxonInfo();
    });
  };

  const getGoatTaxonInfo = () => {
    let newSpeciesTaxonomyId = "";
    httpClient().get('/taxon/' + requestedTaxonomyId, {})
    .then((res: any) => {
      const relationships = res.data.data.relationships;
      newSpeciesTaxonomyId = relationships?.species?.data?.id || '';
      setSpeciesTaxonomyId(newSpeciesTaxonomyId);
      setSpeciesName(relationships?.species?.data?.attributes?.scientific_name || '');
    })
    .catch(() => {})
    .finally(() => {
      if (newSpeciesTaxonomyId === "") {
        PopUpMessage({
          type: "error",
          message: "The Taxonomy ID cannot be found in GoaT or is above species level",
        })
      } else {
        openModal();
      }
    });
  }

  const saveRequest = () => {
    setOpen(false);
    clearAll();
    const json = {
      species_id: speciesTaxonomyId,
      requested_taxonomy_id: requestedTaxonomyId,
      species_name: speciesName,
      specimen_id: specimenId,
    }
    httpClient().post('/request/create', [json], {
    }).then((res: any) => {
      if (res.status === 200) {
        PopUpMessage({
          type: "success",
          message: "ToLID request submitted successfully",
        })
        setForceUpdate(!forceUpdate);
      }
    }).catch((error: any) => {
      console.error(error.message);
      PopUpMessage({
        type: "error",
        message: error.response?.data?.errors?.[0]?.detail ?? 'An error occured. Please try again later.',
      })
    });
  }

  const requestButton = (
    <Button type="success" onClick={saveRequest} icon="arrow-right"/>
  );

  const createRequest = (
    <div>
      <h2 className="sub-heading">Request a ToLID</h2>
      <Form>
        <Form.Group>
          <Form.Control
            value={requestedTaxonomyId}
            onChange={(e) => setRequestedTaxonomyId(e.target.value)}
            placeholder="NCBI Taxonomy ID"
          />
          <p className="form-info">The Taxonomy ID as registered at NCBI. This must be a species-level taxonomy ID.</p>
          <Form.Control
            value={specimenId}
            onChange={(e) => setSpecimenId(e.target.value)}
            id="specimenId"
            placeholder="Specimen ID"
          />
          <p className="form-info">The internal ID of the specimen. This is only used in the ToLID system and should be how you refer to the specimen in your lab</p>
        </Form.Group>
        <Button disabled={requestedTaxonomyId === "" || specimenId === ""} onClick={() => getTolidTaxonInfo()} text={'Request'}/>
      </Form>
      <Modal
        size='md'
        open={open}
        setOpen={setOpen}
        actionButton={requestButton}
      >
        <h2>Confirm ToLID Request</h2>
        <>{requestedTaxonomyId !== speciesTaxonomyId &&
          <StatusMessage
            status={"warning" as TMessageType}
            message={"The requested Taxonomy ID is not species level. The generated ToLID will be for the species: " + speciesName}
          />
        }</>
        <h5 style={{marginTop: 12, marginBottom: 10}}>Are you sure you want to request a ToLID for the following species?</h5>
        <p><strong>Requested Taxonomy ID: </strong><span className='request-value'>{requestedTaxonomyId}</span></p>
        <p><strong>Species Level Taxonomy ID: </strong><span className="request-value">{speciesTaxonomyId}</span></p>
        <p><strong>Species Level Scientific Name: </strong><span className="request-value">{speciesName}</span></p>
        <p><strong>Specimen ID: </strong><span className="request-value">{specimenId}</span></p>
      </Modal>
    </div>
  );

  const specimenZone = useZone({
    objectType: 'specimen',
    dataSource: new TsDataSource(),
    components: [
      {
        id: 'my-tolids',
        filter: {
          and_: {
            'user.id': {
              eq: {
                value: userId
              }
            }
          }
        }
      }
    ],
  });

  const myTolids = (
    <div>
      <h2 className="sub-heading">My ToLIDs</h2>
      <RemoteTable
        id="my-tolids"
        noConfigModal
        noDownload
        height={400}
        fields={{
          data: {
            'id': {
              rename: 'ToLID'
            },
            'specimen_id': {},
            'species.name': {
              rename: 'Species',
              cellRenderer: 'relationship'
            },
            'species.id': {
              rename: 'Taxon ID',
              cellRenderer: {
                element: SubspeciesCellRenderer,
                propPointers: {
                  taxonId: 'species.id',
                  requestedTaxonId: 'requested_taxonomy_id'
                }
              }
            },
            created_at: {}
          },
          order: {
            active: [
              'id',
              'specimen_id',
              'species.name',
              'species.id',
              'created_at'
            ]
          }
        }}
        {...specimenZone}
      />
    </div>
  );

  const requestsZone = useZone({
    objectType: 'request',
    dataSource: new TsDataSource(),
    components: [
      {
        id: 'my-requests',
        filter: {
          and_: {
            'user.id': {
              eq: {
                value: userId
              }
            }
          }
        }
      }
    ],
  });

  const myRequests = (
    <div>
      <h2 className="sub-heading">My Requests</h2>
      <RemoteTable
        id="my-request"
        noDownload
        height={400}
        defaultSort="created_at"
        forceUpdate={forceUpdate}
        fields={{
          data: {
            status: {
              cellRenderer: {
                element: TolidStatus,
                propPointers: {
                  status: 'status',
                  reason: 'reason'
                }
              },
            },
            species_id: {
              rename: "Taxon ID"
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
                  endpoint: 'taxon',
                  attribute: 'scientific_name'
                }
              },
              sort: false
            },
            requested_taxonomy_id: {
              rename: "Requested Taxon ID"
            },
            custom_requested_name: {
              rename: "Requested Scientific Name",
              custom: true,
              cellRenderer: {
                element: DetailAttribute,
                propPointers: {
                  id: 'requested_taxonomy_id'
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
              sort: false
            },
            specimen_id: {
              rename: "Specimen ID",
              sort: false
            },
            created_at: {}
          },
          order: {
            active: [
              'status',
              'species_id',
              'custom_scientific_name',
              'requested_taxonomy_id',
              'custom_requested_name',
              'confirmation_name',
              'specimen_id',
              'created_at'
            ]
          }
        }}
        {...requestsZone}
      />
    </div>
  );

  const components = [
    {
      component: createRequest,
      type: 'full'
    },
    {
      component: myTolids,
      type: 'full'
    },
    {
      component: myRequests,
      type: 'full'
    }
  ];

  return (
    <div className="profile">
      <Widgets
        components={components}
      />
    </div>
  );
}

export default MyTolids;
