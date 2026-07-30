/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Loader, httpClient } from '@tol/tol-ui';
import { useEffect, useState } from 'react';


async function fetchData(id: string, endpoint: string, baseUrl?: string) {
  return await httpClient().get('/' + endpoint + '/' + id, {
    baseURL: baseUrl
  }).then((res: any) => {
    return res;
  }).catch((error: any) => {
    return error;
  });
}

const pendingPromises: {
  [endpoint: string]: Promise<object>
} = {};

const data: {
  [key: string]: {
    [key: string]: number
  }
} = {};

export async function fetchDetail(id: string, endpoint: string, baseUrl?: string): Promise<object> {
  if (!pendingPromises[endpoint]) {
    pendingPromises[endpoint] = Promise.resolve({});
  }
  pendingPromises[endpoint] = pendingPromises[endpoint].then(async () => {
    if (!(endpoint in data)) data[endpoint] = {};
    if (id in data[endpoint]) return data[endpoint][id];
    const retrievedData = await fetchData(id, endpoint, baseUrl);
    data[endpoint][id] = retrievedData;
    return retrievedData;
  });
  return pendingPromises[endpoint];
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
    let cancelled = false;
    fetchDetail(id, endpoint, baseUrl).then((res: any) => {
      if (cancelled) return;
      if ('data' in res
        && 'data' in res.data
        && 'attributes' in res.data.data
      ) {
        if (attribute === 'id') {
          setText(res.data.data.id);
        } else {
          setText(res.data.data.attributes[attribute]);
        }
      } else {
        setText('');
      }
      setLoading(false);
    });
    return () => { cancelled = true; };
  }, [id, endpoint, baseUrl, attribute]);

  return (
    <div className='loading-cell'>
      {loading ?
        <Loader
          size="sm"
          role="status"
          aria-hidden
        />
      :
        text
      }
    </div>
  );
}
