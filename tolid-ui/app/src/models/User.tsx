import { Role } from './Role';

export interface User {
  email: string;
  name: string;
  organisation: string;
  roles: Role[];
}

