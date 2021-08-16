import { Species } from '../../models/Species';
import * as React from 'react';
import { ErrorMessage } from '../../models/ErrorMessage'
import { httpClient } from '../../services/http/httpClient';

import './AddSpecies.scss'

export interface AddSpeciesProps {
}
export interface AddSpeciesState {
    input: string
}

const splitInput = (input: string) => {
    // split on contiguous whitespace (consisting only of "\n" and "\t",
    // NOT spaces, as certain fields can contain spaces)
    const regExp = /[\t\n]{1,}/;
    return input.split(regExp);
}

const parseInput = (input: string): Species => {
    const split = splitInput(input);
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

const postSpecies = (species: Species) => {
    return httpClient().post('/species', species)
        .then((data: any) => {
            return data.data[0] as Request;
        })
        .then((err: any) => {
            return err as ErrorMessage;
        });
}

class AddSpecies extends React.Component<AddSpeciesProps, AddSpeciesState> {
    sendRequest() {
        const species = parseInput(this.state.input);
        const err = postSpecies(species)
        console.log(err);
    }

    public render() {
        return (
            <div>
                <button className="btn btn-primary" id="makeRequestButton" onClick={this.sendRequest}></button>
            </div>
        );
    }
}

export default AddSpecies;
