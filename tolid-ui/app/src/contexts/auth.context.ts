import { createContext, useContext } from 'react';

interface AuthContextValue {
  token: string;
  setToken: (token: string) => void;
  permission: string[];
  setPermission: (permission: string[]) => void;
}

export const AuthContext = createContext<AuthContextValue>({
  token: '',
  setToken() {
    throw new Error('Missing AuthContext Provider');
  },
  permission: [],
  setPermission() {
    throw new Error('Missing AuthContext Provider');
  },
});

export const AuthProvider = AuthContext.Provider;
export const useAuth = () => useContext(AuthContext);
