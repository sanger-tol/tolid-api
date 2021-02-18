export function setTokenToLocalStorage(token: string) {
  localStorage.setItem('token', token);
}

export function getTokenFromLocalStorage() {
  return localStorage.getItem('token') || '';
}
