/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { OverlayTrigger, Pagination, Tooltip } from 'react-bootstrap';
import { Species } from '../../models/Species'
import * as React from 'react'
import { StyledSearchResultsTable } from './SearchResultsTableStyled'
import { ToLID } from '../../models/ToLID';
import { Specimen } from '../../models/Specimen';
import { SearchResultsTableTab } from './SearchResultsTableTab';

interface Props {
    getNextSpeciesPage: () => Promise<void>;
    tolIds: ToLID[];
    specimens: Specimen[];
    species: Species[];
    totalNumSpecies: number;
}

interface State {
    currentTabNum: number;
    requestIsPending: boolean;
}

export enum SearchResultType {
    ToLID,
    Specimen,
    Species
}

const numResultsPerTab = 5;

const LastTabOverlay = (props: any) => (
    <Tooltip id="cannot-go-next-tooltip" className="show" {...props}>
        <p>The end of the results has been reached.</p>
    </Tooltip>
)

const StillFetchingOverlay = (props: any) => (
    <Tooltip id="cannot-go-next-tooltip" className="show" {...props}>
        <p>Search results are still being fetched.</p>
    </Tooltip>
)

export default class SearchResultsTable extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
            currentTabNum: 0,
            requestIsPending: false
        }
    }

    getNumTabs = () => {
        // total number of search results is the sum of the given number of ToLID's,
        // specimens, and the specified _total_ number of species, **not** the given
        // number of species, as they are not all fetched at once
        const totalSearchResults = this.props.tolIds.length +
                                   this.props.specimens.length +
                                   this.props.totalNumSpecies;
        return Math.ceil(totalSearchResults / numResultsPerTab);
    }

    // pairs each search result of any type (ToLID/Specimen/Species) with an enum
    // value indicating its type
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
            const lastPopulatedTab = this.getLastPopulatedTabNumber();
            // the number of tabs to go before the next page should be fetched
            const preloadDifference = 2;
            // if within threshold, get next page
            if (lastPopulatedTab - this.state.currentTabNum < preloadDifference) {
                // if there is already a request in progress, abort
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

    goToPreviousTab = () => {
        // don't decrement below 0
        if (this.state.currentTabNum === 0) return;
        // decrement the current tab number
        this.setState((prevState, prevProps) => ({
            currentTabNum: prevState.currentTabNum - 1
        }));
    }

    isOnFinalTab = () => this.state.currentTabNum === this.getNumTabs() - 1;

    getLastPopulatedTabNumber = () => {
        const numberFetchedSearchResults = this.props.tolIds.length +
                                           this.props.specimens.length +
                                           this.props.species.length;
        const lastPopulatedTab = Math.ceil(
            numberFetchedSearchResults / numResultsPerTab
        );
        return lastPopulatedTab;
    }

    isOnLastPopulatedTab = () => {
        const lastPopulatedTab = this.getLastPopulatedTabNumber();
        return this.state.currentTabNum === lastPopulatedTab - 1;
    }

    canGoToNextTab = () => {
        if (this.isOnFinalTab()) return false;
        if (this.isOnLastPopulatedTab()) return false;
        return true;
    }

    canGoToPreviousTab = () => this.state.currentTabNum !== 0;

    goToNextTab = () => {
        // don't increment above max
        if (!this.canGoToNextTab()) return;
        // increment the current tab number
        this.setState((prevState, prevProps) => ({
            currentTabNum: prevState.currentTabNum + 1
        }));
    }

    public render() {
        return (
            <StyledSearchResultsTable>
                <SearchResultsTableTab
                    searchResults={this.getSearchResultsInCurrentTab()}
                >
                </SearchResultsTableTab>
                <Pagination size="lg" className="d-flex justify-content-center">
                    <Pagination.Prev
                        onClick={this.goToPreviousTab}
                        disabled={!this.canGoToPreviousTab}
                    />
                    {this.canGoToNextTab() ?
                        <Pagination.Next onClick={this.goToNextTab}/>
                        :
                        <OverlayTrigger
                            placement="top"
                            overlay={
                                this.isOnFinalTab() ?
                                LastTabOverlay :
                                StillFetchingOverlay
                            }
                            delay={{ show: 0, hide: 150 }}
                        >
                            <div>
                                <Pagination.Next disabled/>
                            </div>
                        </OverlayTrigger>
                    }
                </Pagination>
                <p className="text-center">
                    Page {this.state.currentTabNum + 1} of {this.getNumTabs()}.
                </p>
            </StyledSearchResultsTable>
        )
    }
}

