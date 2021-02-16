import * as React from 'react';
import { ToLID } from '../../models/ToLID'
import { ErrorMessage } from '../../models/ErrorMessage'

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
    fetch('/api/v2/tol-ids/mine', {method: 'GET',
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
              tolIds: [],
              error: res
            })
          } else {
            this.setState({
              tolIds: res,
              error: null
            })
          }
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
            <table className="table table-striped">
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
            </table>
          }
        </div>
      );
    }
  }
  export default UserToLIDsList;