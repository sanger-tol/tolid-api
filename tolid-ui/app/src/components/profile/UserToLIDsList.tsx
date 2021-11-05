/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import * as React from 'react';
import { Table } from "react-bootstrap";
import { ToLID } from '../../models/ToLID'
import { ErrorMessage } from '../../models/ErrorMessage'
import { httpClient } from '../../services/http/httpClient';

import './UserToLIDsList.scss'

export interface Props {
}
export interface State {
    tolIds: ToLID[],
    error: ErrorMessage | null
}

class UserToLIDsList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      tolIds: [],
      error: null
    }
  }
  
  componentDidMount() {
    this.updateToLIDsList();
  }

  updateToLIDsList() {
    httpClient().get('/tol-ids/mine')
      .then((data: any) => {
        console.log(data)
        this.setState({
          tolIds: data.data,
          error: null
        })
      })
      .catch((err: any) => {
        console.log(err)
      })
    
}


  public render() {
      return (
        <div id="userToLIDsList">
            {(this.state.error !== null) &&
            <p className="alert alert-danger">
                {this.state.error.title}: {this.state.error.detail}
            </p>
            }
          
          {this.state.tolIds.length > 0 &&
            <Table responsive striped>
              <thead>
                <tr><th>ToLID</th><th>Taxonomy ID</th><th>Name</th><th>Specimen ID</th></tr>
              </thead>
              <tbody>
                {this.state.tolIds.map((item: ToLID) => (
                  <tr key={item.tolId} className="tolid">
                    <td>{item.tolId}</td>
                    <td>{item.species.taxonomyId}</td>
                    <td>{item.species.scientificName}</td>
                    <td>{item.specimen.specimenId}</td>
                  </tr>
                  ))}
              </tbody>
            </Table>
          }
          {this.state.tolIds.length === 0 &&
            <p>No ToLIDs created by you</p>
          }
        </div>
      );
    }
  }
  export default UserToLIDsList;