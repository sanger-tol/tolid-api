/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import * as React from 'react';
import { Table } from "react-bootstrap";
import { Request } from '../../models/Request'
import { ErrorMessage } from '../../models/ErrorMessage'
import { httpClient } from '../../services/http/httpClient';

import './UserRequestsList.scss'

export interface Props {
}
export interface State {
    requests: Request[],
    error: ErrorMessage | null
}

class UserRequestsList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      requests: [],
      error: null
    }
  }
  
  componentDidMount() {
    this.updateRequestsList();
  }

  updateRequestsList() {
      httpClient().get('/requests/mine')
        .then((data: any) => {
          console.log(data)
          this.setState({
            requests: data.data,
            error: null
          })
        })
        .catch((err: any) => {
          console.log(err)
        })
      
  }


  public render() {
      return (
        <div id="requestsList">
            {(this.state.error !== null) &&
            <p className="alert alert-danger">
                {this.state.error.title}: {this.state.error.detail}
            </p>
            }
          
          {this.state.requests.length > 0 &&
            <Table responsive striped>
              <thead>
                <tr><th>Request ID</th><th>Taxonomy ID</th><th>Name</th><th>Specimen ID</th><th>Status</th></tr>
              </thead>
              <tbody>
                {this.state.requests.map((item: Request) => (
                  <tr key={item.requestId} className="request">
                    <td>{item.requestId}</td>
                    <td>{item.species.taxonomyId}</td>
                    <td>{item.species.scientificName}</td>
                    <td>{item.specimen.specimenId}</td>
                    <td>{item.status} {(item.reason !== null) && " (" + item.reason + ")"}</td>
                  </tr>
                  ))}
              </tbody>
            </Table>
          }
          {this.state.requests.length === 0 &&
            <p>No current ToLID requests by you</p>
          }
        </div>
      );
    }
  }
  export default UserRequestsList;