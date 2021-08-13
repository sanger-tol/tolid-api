import { Species } from '../../models/Species';
import * as React from 'react';

import './AddSpecies.scss'

export interface AddSpeciesProps {
}
export interface AddSpeciesState {
}

class AddSpecies extends React.Component<AddSpeciesProps, AddSpeciesState> {
    splitInput(input: string)  {
        // split on contiguous whitespace (i.e. consiting of "\n" and " ")
        const regExp = /\s{1,}/;
        return input.split(regExp);
    }
}

export default AddSpecies;
