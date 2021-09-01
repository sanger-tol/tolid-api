import React from "react";
import { PrimaryPrefix } from '../../models/PrimaryPrefix'
import { SecondaryPrefix } from "../../models/SecondaryPrefix";
import { httpClient } from '../../services/http/httpClient';

import './PrefixTable.scss'

export interface Props {
}
export interface State {
    primaryPrefix: PrimaryPrefix[],
    err: Boolean
}

class PrefixTable extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      primaryPrefix: [],
      err: false
    }
  }

  componentDidMount() {
    this.createPrefixTable();
  }

  createPrefixTable() {
    httpClient().get('/prefix/all')
      .then((data: any) => {
        console.log(data)
        this.setState({
          primaryPrefix: data.data
        })
      })
      .catch((err: any) => {
        console.log(err)
        this.setState({
          err: true
        })
      })
  }

  render() {
    return (
      <div>
        {(!this.state.err ?
          <table className="table table-striped">
            <thead>
              <tr>
                <th>First prefix</th>
                <th>Second prefix</th>
                <th>Covers</th>
                <th>Covers in detail</th>
              </tr>
            </thead>
            <tbody>
              {this.state.primaryPrefix.map((primary: PrimaryPrefix) => (
                primary.secondaryPrefixes.map((secondary: SecondaryPrefix) => (
                  <tr key={primary.letter.concat(secondary.letter)}>
                    <td>{primary.letter}</td>
                    <td>{secondary.letter}</td>
                    <td>{primary.name}</td>
                    <td>{secondary.name}</td>
                  </tr>
                ))
              ))}
            </tbody>
          </table>
          :
          <p className="msg err">Error: Unable to connect to ToLID database</p>
        )}
        {(this.state.primaryPrefix.length == 0 && !this.state.err &&
          <p className="msg war">Warning: No ToLID prefix data found in database</p>
        )}
      </div>
    );
  }
}

export default PrefixTable;
