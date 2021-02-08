import { Species } from './Species';
import { Specimen } from './Specimen';

export interface ToLID {
  species: Species;
  specimen: Specimen;
  tolId: string;
}

