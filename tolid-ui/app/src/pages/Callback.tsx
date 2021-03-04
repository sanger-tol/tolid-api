import { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuth } from '../contexts/auth.context';
import {getProfile, getToken} from '../services/auth/authService';
import { useQuery } from '../hooks/useQuery';
import { setTokenToLocalStorage } from '../services/localStorage/localStorageService';

export function Callback() {
  const history = useHistory();
  const { setToken, token } = useAuth();
  const [state] = useState(useQuery().get('state') || undefined);
  const [tokenCode] = useState(useQuery().get('code') || undefined);

  useEffect(() => {
    if (!token) {
      const stateToken = {
        state,
        code: tokenCode,
      };
      getToken(stateToken)
        .then((res: any) => {
          const data = res.data;
          getProfile(data.access_token).finally(() => {
            setTokenToLocalStorage(data.access_token);
            setToken(data.access_token);
            let targetUrl = localStorage.getItem('returnUrl') || '';
            if (!targetUrl || targetUrl === 'index') {
              targetUrl = '/';
            }
            history.replace(targetUrl);
          });
        })
        .catch((error) => {
          history.replace('/login');
        });
    }
    // eslint-disable-next-line
  }, []);

  return null;
}

export default Callback