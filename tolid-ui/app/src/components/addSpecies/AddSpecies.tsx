import { Species } from '../../models/Species';
import * as React from 'react';
import { ErrorMessage } from '../../models/ErrorMessage';
import { httpClient } from '../../services/http/httpClient';

import './AddSpecies.scss'

export interface AddSpeciesProps {
    updateRequestsList?: () => void
}
export interface AddSpeciesState {
    additionComplete: boolean;
    lineFailures: string[];
    previouslyCompleted: boolean;
}

const splitInput = (input: string) : string[] => {
    const splitInput = input.split("\n");
    // if the last line is empty, remove it
    if (splitInput[splitInput.length - 1] === "") {
        return splitInput.slice(0, -1);
    }
    return splitInput;
}

const splitLine = (line: string): string[] => {
    // split on contiguous "\t"
    const regExp = /[\t]+/;
    return line.split(regExp);
}

const parseSpecies = (splitLine: string[]): Species => {
    const species = {
        prefix: splitLine[0],
        scientificName: splitLine[1],
        taxonomyId: parseInt(splitLine[2]),
        commonName: splitLine[3],
        genus: splitLine[4],
        family: splitLine[5],
        order: splitLine[6],
        taxaClass: splitLine[7],
        phylum: splitLine[8],
        kingdom: ""
    } as Species;

    return species;
}

const createError = (detail: string): ErrorMessage => {
    return {
        detail: detail,
        title: "Client-Side Validation Error"
    } as ErrorMessage;
}

const createWrongNumberOfFieldsError = (): ErrorMessage => {
    return createError("9 entries must be provided");
}

const createNonIntegralTaxonomyIdError = (): ErrorMessage => {
    return createError("The taxonomy ID (3rd entry) must be an integer");
}

const validateSplitLine = (split: string[]): ErrorMessage | null => {
    if (split.length !== 9) {
        return createWrongNumberOfFieldsError();
    }
    try {
        if (isNaN(parseInt(split[2]))) {
            return createNonIntegralTaxonomyIdError();
        }
    } catch (exception) {
        return createNonIntegralTaxonomyIdError();
    }
    // all good, return null
    return null;
}

const anyLineErrors = (lineErrors: (ErrorMessage | null)[]): boolean => {
    return lineErrors.some(
        error => error !== null
    ) 
}

class AddSpecies extends React.Component<AddSpeciesProps, AddSpeciesState> {
    constructor(props: AddSpeciesProps) {
        super(props);
        this.state = {
            additionComplete: true,
            lineFailures: [],
            previouslyCompleted: false
        }
    }

    anyClientSideErrors = (splitLines: string[][]): boolean => {
        const clientSideErrors = splitLines.map(
            splitLine => validateSplitLine(splitLine)
        )
        if (anyLineErrors(clientSideErrors)) {
            this.setState(
                (prevState: AddSpeciesState) => ({
                    additionComplete: true,
                    lineFailures: clientSideErrors.map(
                        (error, index) => error === null
                            ? ""
                            : "Validation error on line "
                                + (index + 1).toString() + ": <" 
                                + error.detail + ">."
                    )
                    .filter(
                        error => error !== ""
                    )
                })
            )
            return true;
        }
        return false;
    }

    addLinePostFailure = (lineNumber: number, postError: ErrorMessage) => {
        this.setState((oldState: AddSpeciesState) => ({
            lineFailures: [...oldState.lineFailures].concat([
                "Line " + (lineNumber + 1).toString() + " failed: <"
                    + postError.detail + ">."
            ])
        }));
    }

    postSpecies = async (species: Species[]) => {
        for (let i = 0; i < species.length; i++) {
            await httpClient().post('/species', species[i])
            .catch(
                async (err: any) => {
                    this.addLinePostFailure(
                        i,
                        err.response.data as ErrorMessage
                    );
                }
            )
        }
        this.setState((oldState: AddSpeciesState) => ({
            additionComplete: true
        }));
        this.updateRequestsList();
    }

    postSplitLines = async (splitLines: string[][]) => {
        const species = splitLines.map(
            splitLine => parseSpecies(splitLine)
        );
        if (species.length === 0) {
            this.setState((oldState: AddSpeciesState) => ({
                additionComplete: true,
                lineFailures: [
                    "No species data was provided."
                ]
            }));
        }
        else {
            await this.postSpecies(species);
        }
    }

    splitLines = (): string[][] => {
        const input = document.getElementById("add-species-input") as HTMLInputElement;
        return splitInput(input.value).map(
            line => splitLine(line)
        );
    }

    sendRequest = async (event: any) => {
        event.preventDefault();
        this.setState((oldState: AddSpeciesState) => ({
            additionComplete: false,
            lineFailures: [],
            previouslyCompleted: true
        }));
        const splitLines = this.splitLines();
        if (this.anyClientSideErrors(splitLines)) return;
        await this.postSplitLines(splitLines);
    }

    updateRequestsList = () => {
        if (this.props.updateRequestsList) {
            this.props.updateRequestsList();
        }
    }

    public render() {
        return (
            <div id="add-species-container">
                <form className="form mb-3" id="add-species-form">
                    <div className="form-group">
                        <textarea 
                            className={
                                "form-control form-control-lg"
                                + (this.state.lineFailures.length > 0
                                   ? " is-invalid"
                                   : "")
                            }
                            id="add-species-input"
                            placeholder="Species data..."
                        >
                        </textarea>
                        <small className="form-text text-muted">
                            Adds new species to the database.
                        </small>
                    </div>
                    <button 
                        className={
                            "btn btn-primary" 
                            + (!this.state.additionComplete
                               ? " disabled"
                               : "")
                        }
                        id="add-species-button"
                        onClick={this.sendRequest}
                    >
                        Add Species
                    </button>
                </form>
                {
                    this.state.previouslyCompleted &&
                    this.state.additionComplete && 
                    (this.state.lineFailures.length > 0
                        ?
                        <p className="alert alert-danger">
                            {this.state.lineFailures.map(
                                failure => (
                                    <div>
                                        {failure}
                                        <br></br>
                                    </div>
                                )
                            )
                            }
                        </p>
                        :
                        <p className="alert alert-success">
                            All species successfully added.
                        </p>
                    )
                }
            </div>
        );
    }
}

export default AddSpecies;
