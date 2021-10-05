import * as React from 'react';
import { Request } from '../../models/Request'
import { ErrorMessage } from '../../models/ErrorMessage'
import { Species } from '../../models/Species';
import { httpClient } from '../../services/http/httpClient';
import { OverlayTrigger, Tooltip, Table } from 'react-bootstrap';
import { NcbiData } from '../../models/NcbiData';
import RejectModal from './RejectModal'

import './RequestsList.scss'

const tick = () => (
  <span className="match tick">
    &nbsp;
    {String.fromCharCode(0x2714)}
    &nbsp;
  </span>
)

const cross = () => (
  <span className="match cross">
    &nbsp;
    {String.fromCharCode(0x2718)}
    &nbsp;
  </span>
)

const synonymMatch = () => (
  <span className="match synonym">
    &nbsp;
    {String.fromCharCode(0x2714)}
    &nbsp;
  </span>
)

const getSynonymsForId = async (taxonomyID: number): Promise<string[]> => {
  return httpClient().get('/species/'
                    + taxonomyID.toString()
                    + '/ncbi')
        .then((data: any) => {
          const body: NcbiData = data.data;
          return body.synonyms.concat([body.scientificName]).map(
            (synonym: string) => synonym.toLowerCase()
          );
        })
        .catch((err: any) => {
          return [];
        });
}

const confirmationMatchesSpecies = (confirmationName: string, species?: Species): boolean => {
  if (species === undefined) return false;
  const scientificName = (species.scientificName ?? "").toLowerCase();
  return scientificName === confirmationName;
}

const getSymbol = (request: Request) => {
  const confirmation = (request.confirmationName ?? "").toLowerCase();
  if (confirmation === "") return cross();
  if (confirmationMatchesSpecies(confirmation, request.species)) return tick();
  if (request.synonyms === undefined || request.synonyms.length === 0) return cross();
  if (request.synonyms.includes(confirmation)) return synonymMatch();
  return cross();
}

const getSynonyms = async (data: Request[]): Promise<Request[]> => {
  const newRequests: Promise<Request>[] = data.map(async (request: Request) => {
    if (request.confirmationName !== "" &&
        request.confirmationName !== undefined &&
        request.species.scientificName !== request.confirmationName) {
            request.synonyms = await getSynonymsForId(request.species.taxonomyId);
        }
    return request;
  });
  return await Promise.all(newRequests);
}

const noConfirmationName = () => (
  <i>
    None
  </i>
)

const ConfirmationOverlay = (props: any) => (
    <Tooltip id="confirmation-tooltip" className="show" {...props}>
      Entered during the request creation, as confirmation.
      <br></br>
      {tick()} - The confirmation matches
      <br></br>
      {synonymMatch()} - The confirmation matches a synonym
      <br></br>
      {cross()} - The confirmation does not match
    </Tooltip>
)

export interface Props {
  openAddSpeciesTab?: () => void,
  numSpeciesAdded?: number
}
export interface State {
    requests: Request[],
    error: ErrorMessage | null,
    message: string,
    synonymsLoaded: boolean,
    modal: boolean,
    requestId: number
}

class RequestsList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      requests: [],
      error: null,
      message: '',
      synonymsLoaded: false,
      modal: false,
      requestId: -1
    };
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
              this.setState((oldState: State) => ({
                requests: data.data,
                error: null,
                synonymsLoaded: false
              }));
          })
        .catch((err: any) => {
            this.setState((oldState: State) => ({
              requests: [],
              error: err
            }))
        })
        .finally(() => {
          getSynonyms(this.state.requests).then((requests: Request[]) => {
            this.setState((oldState: State) => ({
              requests: requests,
              synonymsLoaded: true
            }));
          });
        });
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

  addSpecies = () => {
    if (this.props.openAddSpeciesTab) {
      this.props.openAddSpeciesTab();
    }
  }

  toggleModal = () => {
    this.setState({
      modal: !this.state.modal
    });
  }

  setRequestId = (requestId: number) => {
    this.setState({
      requestId: requestId
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
            <Table responsive striped>
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
                    <td>
                      {item.confirmationName ?? noConfirmationName()} 
                      &nbsp;
                      {this.state.synonymsLoaded && getSymbol(item)}
                    </td>
                    <td>{item.specimen.specimenId}</td>
                    <td>{item.createdBy.name}</td>
                    <td>{item.species.prefix}{item.species.currentHighestTolidNumber ? item.species.currentHighestTolidNumber + 1 : 1}</td>
                    <td>
                      {item.species.scientificName ?
                        <button className="btn btn-sm btn-success" onClick={this.acceptRequest} data-request-id={item.requestId}>Accept</button>
                        :
                        <button className="btn btn-sm btn-secondary" onClick={this.addSpecies}>Add Species</button>
                      }
                      <button className="btn btn-sm btn-danger" onClick={() => {this.toggleModal(); this.setRequestId(item.requestId)}}>Reject</button>
                    </td>
                  </tr>
                  ))}
              </tbody>
            </Table>
          }
          <RejectModal
            show={this.state.modal}
            toggle={this.toggleModal.bind(this)}
            requestId={this.state.requestId}
          />
        </div>
    );
  }
}

export default RequestsList;