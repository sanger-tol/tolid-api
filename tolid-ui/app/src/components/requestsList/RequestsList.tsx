import * as React from 'react';
import { Request } from '../../models/Request'
import { ErrorMessage } from '../../models/ErrorMessage'

import './RequestsList.scss'

export interface Props {
}
export interface State {
    requests: Request[],
    error: ErrorMessage | null
}

class RequestsList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      requests: [],
      error: null
    }
  }
  
  componentDidMount() {
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

  public render() {
      return (
        <div id="requestsList">
            {(this.state.error !== null) &&
            <p className="alert alert-danger">
                {this.state.error.title}: {this.state.error.detail}
            </p>
            }
          
          {this.state.requests.length > 0 &&
            <table className="table table-striped">
              <thead>
                <tr><th>Request ID</th><th>Taxonomy ID</th><th>Name</th><th>Requested by</th></tr>
              </thead>
              <tbody>
                {this.state.requests.map((item: Request) => (
                  <tr key={item.id} className="request">
                    <td>{item.id}</td>
                    <td>{item.species.taxonomyId}</td>
                    <td>{item.species.scientificName}</td>
                    <td>{item.createdBy.name}</td>
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