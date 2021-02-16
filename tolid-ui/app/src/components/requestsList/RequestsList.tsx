import * as React from 'react';
import { Request } from '../../models/Request'
import { ErrorMessage } from '../../models/ErrorMessage'

import './RequestsList.scss'

export interface Props {
}
export interface State {
    requests: Request[],
    error: ErrorMessage | null,
    message: string
}

class RequestsList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      requests: [],
      error: null,
      message: ''
    }
  }
  
  componentDidMount() {
    this.updateRequestsList();
  }

  updateRequestsList() {
    fetch('/api/v2/requests/pending', {method: 'GET',
                            headers: {
                              'Content-Type': 'application/json',
                              'api-key': '1234'
                            }})
        // the JSON body is taken from the response
        .then(res => {
          return res.json();
        })
        .then(res => {
          if ("detail" in res) {
            this.setState({
              requests: [],
              error: res
            })
          } else {
            this.setState({
              requests: res,
              error: null
            })
          }
      })
  }

  acceptRequest = (event: any) => {
    const requestId = event.target.dataset["request-id"];
    fetch('/api/v2/requests/'+requestId+'/accept', {method: 'PATCH',
                            headers: {
                              'Content-Type': 'application/json',
                              'api-key': '1234'
                            }})
        // the JSON body is taken from the response
        .then(res => {
          return res.json();
        })
        .then(res => {
          if ("detail" in res) {
            this.setState({
              error: res
            })
          } else {
            this.setState({
              error: null,
              message: "ToLID "+res[0].tolId+" has been assigned"
            })
            this.updateRequestsList();
          }
      })    
  }

  rejectRequest = (event: any) => {
    const requestId = event.target.dataset["request-id"];
    fetch('/api/v2/requests/'+requestId+'/reject', {method: 'PATCH',
                            headers: {
                              'Content-Type': 'application/json',
                              'api-key': '1234'
                            }})
        // the JSON body is taken from the response
        .then(res => {
          return res.json();
        })
        .then(res => {
          if ("detail" in res) {
            this.setState({
              error: res
            })
          } else {
            this.setState({
              error: null
            })
            this.updateRequestsList();
          }
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
            {(this.state.message) &&
            <p className="alert alert-success">
                {this.state.message}
            </p>
            }
          
          {this.state.requests.length > 0 &&
            <table className="table table-striped">
              <thead>
                <tr><th>Request ID</th><th>Taxonomy ID</th><th>Name</th><th>Specimen ID</th><th>Requested by</th><th>Action</th></tr>
              </thead>
              <tbody>
                {this.state.requests.map((item: Request) => (
                  <tr key={item.id} className="request">
                    <td>{item.id}</td>
                    <td>{item.species.taxonomyId}</td>
                    <td>{item.species.scientificName}</td>
                    <td>{item.specimen.specimenId}</td>
                    <td>{item.createdBy.name}</td>
                    <td>
                      {item.species.scientificName &&
                        <button className="btn btn-sm btn-success" onClick={this.acceptRequest} data-request-id={item.id}>Accept</button>
                      }
                      <button className="btn btn-sm btn-danger" onClick={this.rejectRequest} data-request-id={item.id}>Reject</button>
                    </td>
                  </tr>
                  ))}
              </tbody>
            </table>
          }
        </div>
      );
    }
  }
  export default RequestsList;