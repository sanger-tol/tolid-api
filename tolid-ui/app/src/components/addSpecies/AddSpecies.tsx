import { Species } from '../../models/Species';
import * as React from 'react';
import { ErrorMessage } from '../../models/ErrorMessage';
import { httpClient } from '../../services/http/httpClient';

import './AddSpecies.scss'

export interface AddSpeciesProps {
}
export interface AddSpeciesState {
}

const splitInput = (input: string) => {
    // split on contiguous whitespace (consisting only of "\n" and "\t",
    // NOT spaces, as certain fields can contain spaces)
    const regExp = /[\t\n]{1,}/;
    return input.split(regExp);
}

const parseInput = (split: string[]): Species => {
    const species = {
        prefix: split[0],
        scientificName: split[1],
        taxonomyId: parseInt(split[2]),
        commonName: split[3],
        genus: split[4],
        family: split[5],
        order: split[6],
        taxaClass: split[7],
        phylum: split[8]
    } as Species;
    return species;
}

class AddSpecies extends React.Component<AddSpeciesProps, AddSpeciesState> {
    constructor(props: AddSpeciesProps) {
        super(props);
        this.state = {
            error: null
        };
    }

    postSpecies = async (species: Species) => {
        // return an empty error message, can't possibly return null due to a bug
        // in the typescript compiler causing inference that it's always null,
        // thus preventing compilation
        var errorMessage = {
            detail: "",
            title: ""
        }
        await httpClient().post('/species', species)
            .then((data: any) => {
                // do nothing yet
            })
            .catch(
                (err: any) => {
                    errorMessage = err.response.data as ErrorMessage
                }
            )
        return errorMessage;
    }

    getInputError = (split: string[]) => {
        if (split.length !== 9) {
            return "9 entries must be provided";
        }
        try {
            parseInt(split[2]);
        } catch (exception) {
            return "The taxonomy ID (3rd entry) must be an integer";
        }
        // all good, return null
        return null;
    }

    sendRequest = async (event: any) => {
        event.preventDefault();
        const input = document.getElementById("add-species-input") as HTMLInputElement;
        const form = document.getElementById("add-species-form") as HTMLFormElement;
        const split = splitInput(input.value);
        // client side validation
        const error = this.getInputError(split);
        if (error !== null) {
            this.showErrorMessage(input, error);
            return;
        }
        // parse the species and POST
        const species = parseInput(split);
        const errorMessageDetail = (await this.postSpecies(species)).detail;
        // server side validation
        if (errorMessageDetail !== "") {
            this.showErrorMessage(input, errorMessageDetail);
            return;
        }
        // set the success
        this.setSuccess(input, form);
    }

    showErrorMessage = (input: HTMLInputElement, error: string) => {
        input.classList.add("is-invalid");
        input.setCustomValidity(error);
        input.reportValidity();
    }

    setSuccess = (input: HTMLInputElement, form: HTMLFormElement) => {
        // reset the form
        input.classList.remove("is-invalid");
        form.reset();
    }

    public render() {
        return (
            <div id="add-species-container">
                <form className="form" id="add-species-form">
                    <div className="form-group">
                        <input type="text" className="form-control form-control-lg" id="add-species-input" placeholder="Species data..." />
                        <small className="form-text text-muted">
                            Add a new species to the database.
                        </small>
                    </div>
                    <button className="btn btn-primary" id="add-species-button" onClick={this.sendRequest}>
                        Add Species
                    </button>
                </form>
            </div>
        );
    }
}

export default AddSpecies;
