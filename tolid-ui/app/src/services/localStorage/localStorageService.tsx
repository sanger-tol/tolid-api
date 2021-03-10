import { User } from '../../models/User'

export function setTokenToLocalStorage(token: string) {
  localStorage.setItem('token', token);
}

export function getTokenFromLocalStorage() {
  return localStorage.getItem('token') || '';
}

export function setUserToLocalStorage(user: User|null) {
  if (user === null) {
    localStorage.setItem('user', '');
  }
  localStorage.setItem('user', JSON.stringify(user));
}

export function getUserFromLocalStorage() {
  var user = localStorage.getItem('user') || '{}';
  return JSON.parse(user);
}

export function tokenHasExpired(token: string) {
  try {
    var token_decoded = JSON.parse(atob(token.split('.')[1]));
    if ((token_decoded.exp - 3540) * 1000 < Date.now()) {
      return true;
    }
  } catch (e) {
    return true;
  }
  return false;
}