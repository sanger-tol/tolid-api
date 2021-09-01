import { SecondaryPrefix } from './SecondaryPrefix';

export interface PrimaryPrefix {
    letter: string;
    name: string;
    secondaryPrefixes: SecondaryPrefix[];
}
