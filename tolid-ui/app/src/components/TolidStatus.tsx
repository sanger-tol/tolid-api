/*
SPDX-FileCopyrightText: 2023 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Status } from '@tol/tol-ui';


function statusType(status: string) {
  switch(status) {
  case 'Accepted':
    return 'success';
  case 'Rejected':
    return 'danger';
  default:
    return 'warning';
  }
}

interface Props {
  status: string,
  reason: any
}

function StatusExample(props: Props) {
  const { status, reason } = props;

  return (
    <div>
      <Status
        text={status}
        status={statusType(status)}
      />
      <p style={{fontSize: 12, marginTop: 8}}>Reason: {reason}</p>
    </div>
  );
}

export default StatusExample;
