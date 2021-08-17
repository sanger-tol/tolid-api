import { Species } from '../../models/Species';
import * as React from 'react';
import { ErrorMessage } from '../../models/ErrorMessage';
import { httpClient } from '../../services/http/httpClient';

import './AddSpecies.scss'

export interface AddSpeciesProps {
}
export interface AddSpeciesState {
}

const splitInput = (input: string): string[] => {
    // split on contiguous whitespace (consisting only of "\n" and "\t",
    // NOT spaces, as certain fields can contain spaces)
    const regExp = /[\t\n]{1,}/;
    return input.split(regExp);
}

const parseSpecies = (split: string[]): Species => {
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

const postSpecies = async (species: Species): Promise<ErrorMessage | null> => {
    let errorMessage: ErrorMessage | null = null;
    await httpClient().post('/species', species)
        .catch(
            (err: any) => {
                errorMessage = err.response.data as ErrorMessage
            }
        )
    return errorMessage;
}

const validateInput = (split: string[]): ErrorMessage | null => {
    if (split.length !== 9) {
        return {
           detail: "9 entries must be provided",
           title: "Client-Side Validation Error"
        } as ErrorMessage;
    }
    try {
        parseInt(split[2]);
    } catch (exception) {
        return {
            detail: "The taxonomy ID (3rd entry) must be an integer",
            title: "Client-Side Validation Error"
        } as ErrorMessage;
    }
    // all good, return null
    return null;
}

class AddSpecies extends React.Component<AddSpeciesProps, AddSpeciesState> {
    constructor(props: AddSpeciesProps) {
        super(props);
    }

    sendRequest = async (event: any) => {
        event.preventDefault();
        const input = document.getElementById("add-species-input") as HTMLInputElement;
        const form = document.getElementById("add-species-form") as HTMLFormElement;
        const split = splitInput(input.value);
        // client side validation
        const clientSideError = validateInput(split);
        if (clientSideError !== null) {
            this.showErrorMessage(input, clientSideError);
            return;
        }
        // parse the species and POST
        const species = parseSpecies(split);
        const serverSideError = await postSpecies(species);
        // server side validation
        if (serverSideError !== null) {
            this.showErrorMessage(input, serverSideError);
            return;
        }
        // set the success
        this.setSuccess(input, form);
    }

    showErrorMessage = (input: HTMLInputElement, error: ErrorMessage) => {
        input.classList.add("is-invalid");
        input.setCustomValidity(error.detail);
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
