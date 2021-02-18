import { httpServices } from './httpService';
import { getTokenFromLocalStorage } from '../localStorage/localStorageService';

//let initInterceptors = false;

export function httpClient() {
  const token = getTokenFromLocalStorage();
  const { client, ...http } = httpServices(token);
  return http;
}
