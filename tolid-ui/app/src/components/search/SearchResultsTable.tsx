/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Pagination } from 'react-bootstrap';
import SearchResultsSpecies from './SearchResultsSpecies'
import { Species } from '../../models/Species'
import * as React from 'react'
import { StyledSpeciesTable } from './SpeciesTableStyled'
import { ToLID } from '../../models/ToLID';
import { Specimen } from '../../models/Specimen';
import SearchResultsToLID from './SearchResultsToLID';
import SearchResultsSpecimen from './SearchResultsSpecimen';

interface Props {
    getNextSpeciesPage: () => Promise<void>;
    tolIds: ToLID[];
    specimens: Specimen[];
    species: Species[];
}

interface State {
    currentTabNum: number;
    requestIsPending: boolean;
}

enum SearchResultType {
    ToLID,
    Specimen,
    Species
}

const numResultsPerTab = 10;

export default class SearchResultsTable extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
            currentTabNum: 0,
            requestIsPending: false
        }
    }

    getNumTabs = () => {
        const totalSearchResults = this.props.tolIds.length +
                                   this.props.specimens.length +
                                   this.props.species.length;
        return Math.ceil(totalSearchResults / numResultsPerTab);
    }

    getAllSearchResults = () => {
        const searchResultTypes: SearchResultType[] = Array(this.props.tolIds.length)
            .fill(SearchResultType.ToLID)
            .concat(
                Array(this.props.specimens.length).fill(SearchResultType.Specimen),
                Array(this.props.species.length).fill(SearchResultType.Species)
            );
        const searchResults = (this.props.tolIds as Array<ToLID | Specimen | Species>)
            .concat(
                this.props.specimens,
                this.props.species
            );
        // pair each search result with its enum type, into an array
        const pairedSearchResults = searchResults.map(
            (_, index) => [
                searchResults,
                searchResultTypes
            ].map(
                elements => elements[index]
            ) 
        ) as Array<[ToLID | Specimen | Species, SearchResultType]>;

        return pairedSearchResults;
    }

    getSearchResultsInCurrentTab = () => 
        this.getAllSearchResults().slice(
            this.state.currentTabNum * numResultsPerTab,
            (this.state.currentTabNum + 1) * numResultsPerTab
        )

    componentDidUpdate(prevProps: Props, prevState: State) {
        if (this.state.currentTabNum !== prevState.currentTabNum) {
            const numTabs = this.getNumTabs();
            // the number of tabs to go before the next page should be fetched
            const preloadDifference = 2;
    
            // if within threshold, get next page
            if (numTabs - this.state.currentTabNum < preloadDifference) {
                // there is already a request in progress, abort
                if (this.state.requestIsPending === true) return;

                // indicate that a request is pending
                this.setState((oldState, oldProps) => ({
                    requestIsPending: true
                }));
                // get next page of species
                this.props.getNextSpeciesPage()
                    .then(() => {
                        // indicate that the request has finished
                        this.setState((oldState, oldProps) => ({
                            requestIsPending: false
                        }));
                    });
            }
        }
    }

    getSearchResultView = (searchResultPair: [ToLID | Specimen | Species, SearchResultType]) => {
        const searchResultType = searchResultPair[1];
        const searchResult = searchResultPair[0];
        switch (searchResultType) {
            case SearchResultType.ToLID:
                return (
                    <SearchResultsToLID tolid={searchResult as ToLID} />
                )
            case SearchResultType.Specimen:
                return (
                    <SearchResultsSpecimen specimen={searchResult as Specimen} />
                )
            case SearchResultType.Species:
                return (
                    <SearchResultsSpecies species={searchResult as Species} />
                )
        }
    }

    public render() {
        return (
            <StyledSpeciesTable>
                {this.props.species &&
                    this.getSearchResultsInCurrentTab().map(
                        (searchResult: [ToLID | Specimen | Species, SearchResultType]) => 
                            this.getSearchResultView(searchResult)
                    )
                }
            </StyledSpeciesTable>
        )
    }
}

