import * as React from 'react';
import { Request } from '../../models/Request'
import { ErrorMessage } from '../../models/ErrorMessage'
import { httpClient } from '../../services/http/httpClient';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

import './RequestsList.scss'

const ConfirmationOverlay = (props: any) => (
    <Tooltip id="confirmation-tooltip" className="show" {...props}>
      Entered during the request creation. Compare to the "Name" column.
    </Tooltip>
)

export interface Props {
  openAddSpeciesTab?: () => void,
  numSpeciesAdded?: number
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
      message: '',
    }
  }

  componentDidUpdate(prevProps: Props, prevState: State) {
    // update requests if a new species has been added
    if (this.props.numSpeciesAdded && prevProps.numSpeciesAdded !== this.props.numSpeciesAdded) {
      this.updateRequestsList();
    }
  }
  
  componentDidMount() {
    this.updateRequestsList();
  }

  updateRequestsList() {
    httpClient().get('/requests/pending')
        .then(data => {
            this.setState({
              requests: data.data,
              error: null
            })
          })
        .catch((err: any) => {
            this.setState({
              requests: [],
              error: err
            })
        })
  }

  acceptRequest = (event: any) => {
    const requestId = event.target.getAttribute("data-request-id");
    httpClient().patch('/requests/'+requestId+'/accept', {})
        // the JSON body is taken from the response
        .then(data => {
            this.setState({
              error: null,
              message: "ToLID "+data.data[0].tolId+" has been assigned"
            })
          })
        .catch((err: any) => {
            this.setState({
              error: err
            })
          })
        .finally(() => {
          this.updateRequestsList();
        })    
  }

  rejectRequest = (event: any) => {
    const requestId = event.target.getAttribute("data-request-id");
    httpClient().patch('/requests/'+requestId+'/reject', {})
          .then(data => {
            this.setState({
              error: null,
              message: "Request "+data.data[0].requestId+" has been rejected"
            })
          })
        .catch((err: any) => {
            this.setState({
              error: err
            })
          })
        .finally(() => {
          this.updateRequestsList();
        })   
  }

  addSpecies = (event: any) => {
    if (this.props.openAddSpeciesTab) {
      this.props.openAddSpeciesTab();
    }
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
                <tr>
                  <th>Request ID</th>
                  <th>Taxonomy ID</th>
                  <th>Name</th>
                  <th>
                  <OverlayTrigger
                    placement="top"
                    overlay={ConfirmationOverlay}
                    delay={{ show: 0, hide: 300 }}
                  >
                    <div>
                      Name Confirmation
                    </div>
                  </OverlayTrigger>
                  </th>
                  <th>Specimen ID</th>
                  <th>Requested by</th>
                  <th>Next ToLID</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {this.state.requests.map((item: Request) => (
                  <tr key={item.requestId} className="request">
                    <td>{item.requestId}</td>
                    <td>{item.species.taxonomyId}</td>
                    <td>{item.species.scientificName}</td>
                    <td>{item.confirmationName ?? ""}</td>
                    <td>{item.specimen.specimenId}</td>
                    <td>{item.createdBy.name}</td>
                    <td>{item.species.prefix}{item.species.currentHighestTolidNumber ? item.species.currentHighestTolidNumber + 1 : 1}</td>
                    <td>
                      {item.species.scientificName ?
                        <button className="btn btn-sm btn-success" onClick={this.acceptRequest} data-request-id={item.requestId}>Accept</button>
                        :
                        <button className="btn btn-sm btn-secondary" onClick={this.addSpecies}>Add Species</button>
                      }
                      <button className="btn btn-sm btn-danger" onClick={this.rejectRequest} data-request-id={item.requestId}>Reject</button>
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