/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import * as React from 'react';
import { ToLID } from '../../models/ToLID'
import { Species } from '../../models/Species'
import { Specimen } from '../../models/Specimen'
import { SpeciesPage } from '../../models/SpeciesPage';
import SearchResultsTable from './SearchResultsTable';
import './SearchResults.scss'

export interface Props {
    list?: string[]
}
export interface State {
    tolids: ToLID[],
    speciess: Species[];
    specimens: Specimen[],
    searchTermIsValid: boolean,
    totalNumSpecies: number
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
function getSpeciessPage(searchTerm: string, page: number): Promise<SpeciesPage> {
    return fetch(
      `/api/v2/species?taxonomyId=${searchTerm}&genus=${searchTerm}&prefix=${searchTerm}&scientificNameFragment=${searchTerm}&page=${page}`
    )
        // the JSON body is taken from the response
        .then(res => {
            if (res.ok) { 
                return res.json();
            }
            return {
                species: [],
                totalNumSpecies: 0
            }; 
          })
        .then(res => {
            return res as SpeciesPage;
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
        specimens: [],
        searchTermIsValid: true,
        totalNumSpecies: 0
      }
    }

    resetForm = (form: HTMLFormElement) => {
      // Finally, we need to reset the form
      this.setState({searchTermIsValid: true});
      form.reset();
    }

    // add a page to the array of species
    joinSpeciess = (speciesPage: SpeciesPage) => {
      this.setState((oldState, oldProps) => ({
        speciess: oldState.speciess.concat(speciesPage.species),
        totalNumSpecies: speciesPage.totalNumSpecies
      }))
    }

    doSearch = (event: any) => {
        event.preventDefault();
        const searchTerm = document.getElementById("searchInput") as HTMLInputElement;
        const form = document.getElementById("searchForm") as HTMLFormElement;
        // If our input has a value
        if (searchTerm.value !== "") {
          // reset the paged results
          this.setState((oldState, oldProps) => ({
            speciess: [],
          }));
          getToLIDs(searchTerm.value)
            .then(tolids => this.setState({ tolids: tolids }));
          getSpecimens(searchTerm.value)
            .then(specimens => this.setState({ specimens: specimens }));
          getSpeciessPage(searchTerm.value, 0)
            .then(speciesPage => this.joinSpeciess(speciesPage));
          this.resetForm(form);
        } else {
          this.setState({searchTermIsValid: false})
        }
    }

    public render() {
      return (
        <div>
            <form className="form" id="searchForm">
                <div className="form-group">
                    <input
                      type="text"
                      className={"form-control form-control-lg" + this.state.searchTermIsValid ? "" : " is-invalid"}
                      id="searchInput"
                      placeholder="Search..."
                    />
                    <small className="form-text text-muted">
                        Search on ToLID prefix (e.g. mHomSap), taxonomy ID (e.g. 9606), species name (e.g. Homo sapiens) or ToLID (e.g. mHomSap1)
                    </small>
                </div>
                <button className="btn btn-primary" id="searchButton" onClick={this.doSearch}>
                Search
                </button>
            </form>
            <ul className="searchResults">
                <SearchResultsTable
                  getNextSpeciesPage={() => Promise.resolve()}
                  tolIds={this.state.tolids}
                  specimens={this.state.specimens}
                  species={this.state.speciess}
                />
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