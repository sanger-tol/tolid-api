/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCheck, faPlus, faXmark, faInfo } from '@fortawesome/free-solid-svg-icons'
import { Button } from '@tol/tol-ui'

type Variant = 'add' | 'accept' | 'reject'

interface Props {
    onClick: () => void | undefined;
    disabled?: boolean;
    variant: Variant;
    text?: string;
}

const variantToIcon = (variant: Variant | string) => {
    switch (variant) {
        case 'add':
            return faPlus
        case 'accept':
            return faCheck
        case 'reject':
            return faXmark
        default:
            return faInfo
    }
}

const variantToStyle = (variant: Variant | string) => {
    switch (variant) {
        case 'add':
            return 'warning'
        case 'accept':
            return 'success'
        case 'reject':
            return 'danger'
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
            <Button onClick={onClick} disabled={disabled} type="button" className="generic-button-wrapper" variant={styling}>
                <div className="pending-button-styling">
                    <FontAwesomeIcon icon={variantToIcon(variant)} />
                    {text}
                </div>
            </Button>
        </div>
    )
}

export default GenericRequestBtn;