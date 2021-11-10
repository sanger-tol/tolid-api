/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import * as React from 'react';
import { ToLID } from '../../models/ToLID'
import { Species } from '../../models/Species'
import { Specimen } from '../../models/Specimen'
import SearchResultsToLID from './SearchResultsToLID'
import SearchResultsSpecies from './SearchResultsSpecies'
import SearchResultsSpecimen from './SearchResultsSpecimen'
import './SearchResults.scss'

export interface Props {
    list?: string[]
}
export interface State {
    tolids: ToLID[],
    speciess: Species[],
    specimens: Specimen[],
}

function getToLIDs(searchTerm: string): Promise<ToLID[]> {
    return fetch('/api/v2/tol-ids/'+searchTerm)
        // the JSON body is taken from the response
        .then(res => {
            if (res.ok) { 
             return res.json();
            }
            return []; 
          })
        .then(res => {
            return res as ToLID[]
        })
}
function getSpeciess(searchTerm: string): Promise<Species[]> {
    return fetch('/api/v2/species?taxonomyId='+searchTerm+'&scientificName='+searchTerm+'&prefix='+searchTerm)
        // the JSON body is taken from the response
        .then(res => {
            if (res.ok) { 
             return res.json();
            }
            return []; 
          })
        .then(res => {
            return res as Species[]
        })
}
function getSpecimens(searchTerm: string): Promise<Specimen[]> {
    return fetch('/api/v2/specimens/'+searchTerm)
        // the JSON body is taken from the response
        .then(res => {
            if (res.ok) { 
             return res.json();
            }
            return []; 
          })
        .then(res => {
            return res as Specimen[]
        })
}

class SearchResults extends React.Component<Props, State> {
    constructor(props: Props) {
      super(props);
      this.state = {
        tolids: [],
        speciess: [],
        specimens: []
      }
    }

    doSearch = (event: any) => {
        event.preventDefault();
        const searchTerm = document.getElementById("searchInput") as HTMLInputElement;
        const form = document.getElementById("searchForm") as HTMLFormElement;
        // If our input has a value
        if (searchTerm.value !== "") {
          getToLIDs(searchTerm.value)
            .then(tolids => this.setState({ tolids: tolids }));
          getSpeciess(searchTerm.value)
            .then(speciess => this.setState({ speciess: speciess }));
          getSpecimens(searchTerm.value)
            .then(specimens => this.setState({ specimens: specimens }))
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
                <div className="form-group">
                    <input type="text" className="form-control form-control-lg" id="searchInput" placeholder="Search..." />
                    <small className="form-text text-muted">
                        Search on ToLID prefix (e.g. mHomSap), taxonomy ID (e.g. 9606), species name (e.g. Homo sapiens) or ToLID (e.g. mHomSap1)
                    </small>
                </div>
                <button className="btn btn-primary" id="searchButton" onClick={this.doSearch}>
                Search
                </button>
            </form>
            <ul className="searchResults">
                {this.state.tolids.map((item: ToLID) => (
                <li key={item.tolId} className="searchResult"><SearchResultsToLID tolid={item}/></li>
                ))}
                {this.state.speciess.map((item: Species) => (
                <li key={item.taxonomyId} className="searchResult"><SearchResultsSpecies species={item}/></li>
                ))}
                {this.state.specimens.map((item: Specimen) => (
                <li key={item.specimenId} className="searchResult"><SearchResultsSpecimen specimen={item}/></li>
                ))}
            </ul>
            {this.state.tolids.length === 0 && this.state.speciess.length === 0 && this.state.specimens.length === 0 &&
            <p>
                No results found
            </p>
            }
        </div>
      );
    }
  }
  export default SearchResults;