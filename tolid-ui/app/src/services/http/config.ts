// SPDX-FileCopyrightText: 2021 Genome Research Ltd.
//
// SPDX-License-Identifier: MIT

export const CONFIG = {
  baseURL: '/api/v2',
  headers: {
    'Content-Type': 'application/json',
  },
};

export const END_POINT = {
  authUrlElixir: '/auth/login',
  authToken: '/auth/token',
  authProfile: '/auth/profile',
  authLogout: '/auth/logout',
};
