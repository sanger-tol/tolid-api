/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import GenericRequestBtn from "./GenericRequestBtn";
import { Link } from "react-router-dom";

function AddSpeciesBtn() {
    return (
        <>
            <Link to="/add-species">
                <GenericRequestBtn
                    variant="add"
                    text="Add"
                />
            </Link>
        </>
    )
}

export default AddSpeciesBtn;