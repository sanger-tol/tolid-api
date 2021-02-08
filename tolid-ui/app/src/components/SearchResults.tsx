import * as React from 'react';
import { ToLID } from '../models/ToLID'
import SearchResultsToLID from './SearchResultsToLID'

export interface Props {
    list?: string[]
}
export interface State {
    list: ToLID[]
}
function getToLIDs(searchTerm: string): Promise<ToLID[]> {
    return fetch('/api/v2/tol-ids/'+searchTerm)
        // the JSON body is taken from the response
        .then(res => res.json())
        .then(res => {
            return res as ToLID[]
        })
}


class SearchResults extends React.Component<Props, State> {
    constructor(props: Props) {
      super(props);
      this.state = {
        list: []
      }
    }

    doSearch = (event: any) => {
        event.preventDefault();
        const searchTerm = document.getElementById("searchInput") as HTMLInputElement;
        const form = document.getElementById("searchForm") as HTMLFormElement;
        // If our input has a value
        if (searchTerm.value !== "") {
          getToLIDs(searchTerm.value)
            .then(tolIDs => this.setState({ list: tolIDs }));
          // Finally, we need to reset the form
          searchTerm.classList.remove("is-invalid");
          form.reset();
        } else {
          // If the input doesn't have a value, make the border red since it's required
          searchTerm.classList.add("is-invalid");
        }
    };

    public render() {
      return (
        <div>
            <form className="form" id="searchForm">
                <input type="text" className="input" id="searchInput" placeholder="Search..." />
                <button className="button is-info" onClick={this.doSearch}>
                Search
                </button>
            </form>
            <ul>
            {this.state.list.map((item: ToLID) => (
            <li key={item.tolId}><SearchResultsToLID tolid={item}/></li>
            ))}
            </ul>
        </div>
      );
    }
  }
  export default SearchResults;