/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Loader, httpClient } from '@tol/tol-ui';
import { useEffect, useState } from 'react';

const cache = new Map<string, Promise<any>>();

function fetchCached(id: string, endpoint: string, baseUrl?: string): Promise<any> {
  const key = `${endpoint}:${id}`;
  if (!cache.has(key)) {
    cache.set(
      key,
      httpClient()
        .get(`/${endpoint}/${id}`, { baseURL: baseUrl })
        .catch(() => null)
    );
  }
  return cache.get(key)!;
}

export function fetchDetail(id: string, endpoint: string, baseUrl?: string): Promise<any> {
  return fetchCached(id, endpoint, baseUrl);
}

interface Props {
  id: string,
  endpoint: string,
  baseUrl?: string,
  attribute: string
}

export function DetailAttribute(props: Props) {
  const { id, endpoint, baseUrl, attribute } = props;
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }
    let cancelled = false;
    fetchCached(id, endpoint, baseUrl)
      .then((res: any) => {
        if (cancelled) return;
        const d = res?.data?.data;
        if (attribute === 'id') {
          setText(d?.id ?? '');
        } else {
          setText(d?.attributes?.[attribute] ?? '');
        }
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [id, endpoint, baseUrl, attribute]);

  return (
    <div className='loading-cell'>
      {loading ?
        <Loader size="sm" role="status" aria-hidden />
      :
        text
      }
    </div>
  );
}
