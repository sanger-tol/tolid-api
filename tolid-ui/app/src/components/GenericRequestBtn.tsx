/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Button } from '@tol/tol-ui'

type Variant = 'add' | 'accept' | 'reject'

interface Props {
  onClick?: any;
  disabled?: boolean;
  variant: Variant;
  text?: string;
}

const variantToIcon = (variant: Variant | string) => {
  switch (variant) {
    case 'add':
      return 'plus'
    case 'accept':
      return 'check'
    case 'reject':
      return 'xmark'
    default:
      return 'info'
  }
}

const variantToStyle = (variant: Variant | string) => {
  switch (variant) {
    case 'add':
      return 'warning'
    case 'accept':
      return 'success'
    case 'reject':
      return 'error'
    default:
      return 'primary'
  }
}

function GenericRequestBtn(props: Props) {
  const { onClick, disabled, text } = props;
  const variant = props.variant;
  const styling = variantToStyle(variant);

  return (
    <div className="generic-button-wrapper">
      <Button onClick={onClick} disabled={disabled} className="generic-button-wrapper" type={styling} icon={variantToIcon(variant)} text={text}/>
    </div>
  )
}

export default GenericRequestBtn;