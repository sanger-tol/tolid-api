import { Species } from './Species';
import { Specimen } from './Specimen';
import { User } from './User';

export interface Request {
  id: number;
  status: string;
  createdBy: User;
  species: Species;
  specimen: Specimen;
}

