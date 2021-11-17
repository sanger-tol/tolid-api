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
import { Form } from 'react-bootstrap';

export interface Props {
    list?: string[]
}
export interface State {
    tolids: ToLID[],
    speciess: Species[];
    specimens: Specimen[],
    searchTermIsValid: boolean,
    totalNumSpecies: number,
    searchTerm?: string,
    currentSpeciesPageNum: number,
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
        totalNumSpecies: 0,
        currentSpeciesPageNum: 0
      }
    }

    resetForm = (form: HTMLFormElement) => {
      // Finally, we need to reset the form
      this.setState({searchTermIsValid: true});
      form.reset();
    }

    fetchNextPageIfExists = async () => {
      if (this.state.searchTerm === undefined || this.state.searchTerm === "") {
        return;
      }
      if (this.state.speciess.length >= this.state.totalNumSpecies) {
        return;
      }
      const speciesPage = await getSpeciessPage(
        this.state.searchTerm,
        this.state.currentSpeciesPageNum + 1
      )
      this.joinSpeciess(speciesPage);
      this.setState((oldState, oldProps) => ({
        currentSpeciesPageNum: oldState.currentSpeciesPageNum + 1
      }));
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
        const searchInput = document.getElementById("searchInput") as HTMLInputElement;
        const form = document.getElementById("searchForm") as HTMLFormElement;
        const searchTerm = searchInput.value;
        // If our input has a value
        if (searchTerm !== "") {
          // reset the paged results
          this.setState((oldState, oldProps) => ({
            speciess: [],
            searchTerm: searchTerm
          }));
          getToLIDs(searchTerm)
            .then(tolids => this.setState({ tolids: tolids }));
          getSpecimens(searchTerm)
            .then(specimens => this.setState({ specimens: specimens }));
          getSpeciessPage(searchTerm, 0)
            .then(speciesPage => this.joinSpeciess(speciesPage));
          this.resetForm(form);
        } else {
          this.setState({
            searchTermIsValid: false,
            searchTerm: undefined
          })
        }
    }

    public render() {
      return (
        <div>
            <Form id="searchForm">
                <Form.Group>
                    <Form.Control
                      type="text"
                      className="form-control form-control-lg"
                      id="searchInput"
                      placeholder="Search..."
                      isInvalid={!this.state.searchTermIsValid}
                    />
                    <Form.Label className="form-text text-muted">
                        Search on ToLID prefix (e.g. mHomSap), taxonomy ID (e.g. 9606), species name (e.g. Homo sapiens) or ToLID (e.g. mHomSap1)
                    </Form.Label>
                </Form.Group>
                <button className="btn btn-primary" id="searchButton" onClick={this.doSearch}>
                Search
                </button>
            </Form>
            <ul className="searchResults">
              {(this.state.tolids.length !== 0 || this.state.speciess.length !== 0 || this.state.specimens.length !== 0) &&
                <SearchResultsTable
                  getNextSpeciesPage={this.fetchNextPageIfExists}
                  tolIds={this.state.tolids}
                  specimens={this.state.specimens}
                  species={this.state.speciess}
                  totalNumSpecies={this.state.totalNumSpecies}
                />
              }
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